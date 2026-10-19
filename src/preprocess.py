def clean_and_flatten(raw_lc, window_length: int = 101):
    clean_lc = raw_lc.remove_nans()
    flat_lc, trend_lc = clean_lc.flatten(
        window_length=window_length, return_trend=True
    )
    return clean_lc, flat_lc, trend_lc