import numpy as np
from astropy import constants as const
from astropy import units as u

def fold_and_bin(flat_lc, period, epoch_time, bin_size: float = 0.01):
    folded_lc = flat_lc.fold(period=period, epoch_time=epoch_time)
    binned_lc = folded_lc.bin(time_bin_size=bin_size)
    return folded_lc, binned_lc

def calculate_physical_parameters(
    binned_lc,
    period,
    target_name: str = "TrES-2",
    r_star=1.000 * const.R_sun,
    m_star=0.980 * const.M_sun,
):
    in_transit = (binned_lc.time.value > -0.03) & (binned_lc.time.value < 0.03)
    min_flux = np.nanmin(binned_lc.flux.value[in_transit])
    transit_depth = 1.0 - min_flux

    r_planet = r_star * np.sqrt(transit_depth)
    r_planet_jup = (r_planet / const.R_jup).decompose().value
    r_planet_earth = (r_planet / const.R_earth).decompose().value

    period_seconds = period.to(u.s)
    semi_major_axis = (
        (const.G * m_star * period_seconds**2) / (4 * np.pi**2)
    ) ** (1 / 3)
    semi_major_axis_au = (semi_major_axis / const.au).decompose().value

    return {
        "Target": target_name,
        "Period_days": f"{period.value:.5f}",
        "Transit_Depth_pct": f"{transit_depth * 100:.3f}",
        "Radius_Rjup": f"{r_planet_jup:.3f}",
        "Radius_Rearth": f"{r_planet_earth:.3f}",
        "SemiMajorAxis_AU": f"{semi_major_axis_au:.4f}",
    }