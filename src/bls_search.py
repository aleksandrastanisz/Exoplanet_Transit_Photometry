import numpy as np

def find_transit_period(
    flat_lc,
    min_period: float = 1.5,
    max_period: float = 4.0,
    num_points: int = 10000,
):
    period_grid = np.linspace(min_period, max_period, num_points)
    bls = flat_lc.to_periodogram(
        method="bls", period=period_grid, frequency_factor=5.0
    )

    best_period = bls.period_at_max_power
    best_t0 = bls.transit_time_at_max_power
    best_duration = bls.duration_at_max_power

    return bls, best_period, best_t0, best_duration