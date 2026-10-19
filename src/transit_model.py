def fold_and_bin(flat_lc, period, epoch_time, bin_size: float = 0.01):
    folded_lc = flat_lc.fold(period=period, epoch_time=epoch_time)
    binned_lc = folded_lc.bin(time_bin_size=bin_size)
    return folded_lc, binned_lc
