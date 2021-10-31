from vigorish.enums import PitchType

BATTER_STANCE_SPLITS = ["all", "rhb", "lhb"]


def combine_career_and_yearly_pfx_pitching_metrics_sets(career_pfx, yearly_pfx):
    combined_pfx_metrics = {}
    career_pfx = _convert_career_pfx_to_dict(career_pfx)
    yearly_pfx = _convert_yearly_pfx_to_dict(yearly_pfx)
    all_pitch_types = _get_pitch_types_sorted(career_pfx["all"]["metrics"]["metrics_by_pitch_type"])
    for stance in BATTER_STANCE_SPLITS:
        combined_pfx_metrics[stance] = {0: {}}
        career_metrics_by_pitch_type = career_pfx[stance]["metrics"]["metrics_by_pitch_type"]
        career_pitch_type_percentiles = {p["pitch_type"]: p for p in career_pfx[stance]["percentiles"]}
        for pitch_type in all_pitch_types:
            if pitch_type in career_pfx[stance]["metrics"]["pitch_type"]:
                combined_pfx_metrics[stance][0][pitch_type] = {
                    "metrics": career_metrics_by_pitch_type.get(pitch_type, {}),
                    "percentiles": career_pitch_type_percentiles.get(pitch_type, {}),
                }
                combined_pfx_metrics[stance][0][pitch_type]["percentiles"]["percent"] = career_metrics_by_pitch_type[
                    pitch_type
                ]["percent"]
        all_seasons_played = yearly_pfx["all"]["metrics"].keys()
        for year in list(all_seasons_played):
            combined_pfx_metrics[stance][year] = {}
            season_metrics_by_pitch_type = yearly_pfx[stance]["metrics"][year]["metrics_by_pitch_type"]
            season_pitch_type_percentiles = {p["pitch_type"]: p for p in yearly_pfx[stance]["percentiles"][year]}
            for pitch_type in all_pitch_types:
                if pitch_type in yearly_pfx[stance]["metrics"][year]["pitch_type"]:
                    combined_pfx_metrics[stance][year][pitch_type] = {
                        "metrics": season_metrics_by_pitch_type.get(pitch_type),
                        "percentiles": season_pitch_type_percentiles.get(pitch_type),
                    }
                    combined_pfx_metrics[stance][year][pitch_type]["percentiles"][
                        "percent"
                    ] = season_metrics_by_pitch_type[pitch_type]["percent"]
    return combined_pfx_metrics


def _convert_career_pfx_to_dict(career_pfx):
    career_pfx["all"]["metrics"] = career_pfx["all"]["metrics"].as_dict()
    career_pfx["rhb"]["metrics"] = career_pfx["rhb"]["metrics"].as_dict()
    career_pfx["lhb"]["metrics"] = career_pfx["lhb"]["metrics"].as_dict()
    return career_pfx


def _convert_yearly_pfx_to_dict(yearly_pfx):
    for year, pfx_stats_for_year in yearly_pfx["all"]["metrics"].items():
        yearly_pfx["all"]["metrics"][year] = pfx_stats_for_year.as_dict()
    for year, pfx_stats_for_year in yearly_pfx["rhb"]["metrics"].items():
        yearly_pfx["rhb"]["metrics"][year] = pfx_stats_for_year.as_dict()
    for year, pfx_stats_for_year in yearly_pfx["lhb"]["metrics"].items():
        yearly_pfx["lhb"]["metrics"][year] = pfx_stats_for_year.as_dict()
    return yearly_pfx


def _get_pitch_types_sorted(metrics_by_pitch_type):
    unsorted = list(metrics_by_pitch_type.values())
    return [str(PitchType(m["pitch_type_int"])) for m in sorted(unsorted, key=lambda x: x["percent"], reverse=True)]
