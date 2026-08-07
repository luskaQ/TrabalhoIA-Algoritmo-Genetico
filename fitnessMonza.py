import numpy as np

G = 9.81
RHO = 1.225


def compute_corner_speed_limit(curvature, mass, mu, Cl, A):
    """
    Maximum speed allowed by lateral grip + aero.
    """

    vmax = np.full_like(curvature, 999.0, dtype=float)

    for i, kappa in enumerate(curvature):

        if abs(kappa) < 1e-9:
            continue

        denom = mass * kappa - 0.5 * mu * RHO * Cl * A

        if denom <= 0:
            vmax[i] = 999.0
            continue

        vmax[i] = np.sqrt(
            (mu * mass * G) / denom
        )

    return vmax


def lap_time_simulator(
    curvature,
    ds,
    mass,
    power,
    Cd,
    Cl,
    A,
    mu,
    Crr,
):
    """
    curvature : numpy array [1/m]
    ds        : spacing between points (meters)

    returns:
        lap_time (seconds)
    """

    n = len(curvature)

    vmax = compute_corner_speed_limit(
        curvature,
        mass,
        mu,
        Cl,
        A
    )

    v = vmax.copy()

    # -----------------------
    # FORWARD PASS
    # -----------------------

    for i in range(n - 1):

        speed = max(v[i], 1.0)
        kappa = curvature[i]

        downforce = (
            0.5
            * RHO
            * Cl
            * A
            * speed**2
        )

        Fz = mass * G + downforce

        Fmax = mu * Fz

        Fy = mass * speed**2 * abs(kappa)

        Fx_available = np.sqrt(
            max(Fmax**2 - Fy**2, 0.0)
        )

        Fengine = power / speed

        Fx = min(
            Fengine,
            Fx_available
        )

        Fdrag = (
            0.5
            * RHO
            * Cd
            * A
            * speed**2
        )

        Frr = Crr * mass * G

        Fnet = Fx - Fdrag - Frr

        a = Fnet / mass

        v_candidate = np.sqrt(
            max(
                speed**2 + 2 * a * ds,
                0.0
            )
        )

        v[i + 1] = min(
            v_candidate,
            vmax[i + 1]
        )

    # -----------------------
    # BACKWARD PASS
    # -----------------------

    for i in range(n - 2, -1, -1):

        speed = max(v[i], 1.0)
        kappa = curvature[i]

        downforce = (
            0.5
            * RHO
            * Cl
            * A
            * speed**2
        )

        Fz = mass * G + downforce

        Fmax = mu * Fz

        Fy = mass * speed**2 * abs(kappa)

        Fb_available = np.sqrt(
            max(Fmax**2 - Fy**2, 0.0)
        )

        Fdrag = (
            0.5
            * RHO
            * Cd
            * A
            * speed**2
        )

        Frr = Crr * mass * G

        a_brake = (
            Fb_available
            + Fdrag
            + Frr
        ) / mass

        v_allowed = np.sqrt(
            max(
                v[i + 1]**2
                + 2 * a_brake * ds,
                0.0
            )
        )

        v[i] = min(
            v[i],
            v_allowed
        )

    # -----------------------
    # LAP TIME
    # -----------------------

    lap_time = 0.0

    for i in range(n - 1):

        vavg = (
            v[i]
            + v[i + 1]
        ) / 2

        if vavg > 0:
            lap_time += ds / vavg

    return lap_time

# Monza track length in meters and step size
track_length = 5793
ds = 1.0

# Initialize curvature array (0 = perfectly straight)
curvature = np.zeros(track_length)

# --- 1. VARIANTE DEL RETTIFILO (Turns 1 & 2 Chicane) ---
# Very tight right-then-left cornering sequence to break up the main straight
curvature[1100:1135] = 1 / 12   # Turn 1: Sharp Right (12m radius)
curvature[1145:1180] = -1 / 15  # Turn 2: Sharp Left (15m radius)

# --- 2. CURVA GRANDE / BIASSONO (Turn 3) ---
# Massive, sweeping high-speed right-hander
curvature[1300:1650] = 1 / 300  # Turn 3: Long Right (300m constant radius)

# --- 3. VARIANTE DELLA ROGGIA (Turns 4 & 5 Chicane) ---
# Left-then-right tight chicane after the second long straight section
curvature[2200:2240] = -1 / 25  # Turn 4: Left entry (25m radius)
curvature[2245:2285] = 1 / 30   # Turn 5: Right exit (30m radius)

# --- 4. CURVA DI LESMO 1 (Turn 6) ---
# Fast, medium-radius right-hander
curvature[2550:2630] = 1 / 85   # Turn 6: Medium Right (85m radius)

# --- 5. CURVA DI LESMO 2 (Turn 7) ---
# Tighter right-hander leading onto the long Serraglio straight
curvature[2780:2850] = 1 / 45   # Turn 7: Tight Right (45m radius)

# --- 6. CURVA DEL SERRAGLIO (Turn 8) ---
# A very gentle, high-speed kink to the left midway through the straight
curvature[3350:3500] = -1 / 1200 # Turn 8: Ultra-wide Left (1200m radius)

# --- 7. VARIANTE ASCARI (Turns 9, 10 & 11) ---
# Famous multi-apex complex: quick left, fast right, sweeping left exit
curvature[3850:3890] = -1 / 60  # Turn 9: Left entry (60m radius)
curvature[3910:3950] = 1 / 45   # Turn 10: Quick Right transition (45m radius)
curvature[3970:4040] = -1 / 100 # Turn 11: Long Left exit (100m radius)

# --- 8. CURVA ALBORETO / PARABOLICA (Turn 12) ---
# Famous 180° final turn featuring a decreasing/increasing parabolic layout.
# We model the opening radius mathematically from tight entry to wide exit.
parabolica_entry = 5120
parabolica_exit = 5450
num_points = parabolica_exit - parabolica_entry

# Radii transitions progressively from 50m out to 220m
parabolica_radii = np.linspace(50, 220, num_points)
curvature[parabolica_entry:parabolica_exit] = 1 / parabolica_radii


lap_time = lap_time_simulator(
    curvature=curvature,
    ds=1.0,
    mass=800,
    power=745700,
    Cd=0.8,
    Cl=2.5,
    A=0.6,
    mu=3,
    Crr=0.02,
)

print(f"Lap time: {lap_time:.2f} s")