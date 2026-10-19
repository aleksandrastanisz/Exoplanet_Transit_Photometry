import lightkurve as lk

def download_data(target_name: str, quarter: int):
    search_result = lk.search_lightcurve(
        target_name, mission="Kepler", quarter=quarter
    )
    if len(search_result) == 0:
        raise ValueError(f"brak danych dla: {target_name}")
    return search_result.download()