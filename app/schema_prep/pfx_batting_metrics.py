from vigorish.enums import PitchType


BATTER_STANCE_SPLITS = [
    "vs_all",
    "vs_rhp",
    "vs_lhp",
    "as_rhb_vs_rhp",
    "as_rhb_vs_lhp",
    "as_lhb_vs_rhp",
    "as_lhb_vs_lhp",
]

PERCENTILE_SPLITS = [
    "vs_all",
    "vs_rhp",
    "vs_lhp",
]


def combine_career_and_yearly_pfx_batting_metrics_sets(career_pfx, yearly_pfx):
    combined_pfx_metrics = {}
    batter_pfx_percentiles = {}
    career_pfx = _convert_career_pfx_to_dict(career_pfx)
    yearly_pfx = _convert_yearly_pfx_to_dict(yearly_pfx)
    all_pitch_types = _get_pitch_types_sorted(career_pfx["vs_all"]["metrics"]["metrics_by_pitch_type"])
    for stance in BATTER_STANCE_SPLITS:
        combined_pfx_metrics[stance] = {0: {}}
        if stance in PERCENTILE_SPLITS:
            batter_pfx_percentiles[stance][0]["percentiles"] = career_pfx[stance]["percentiles"]
        career_metrics_by_pitch_type = career_pfx[stance]["metrics"]["metrics_by_pitch_type"]
        for pitch_type in all_pitch_types:
            if pitch_type in career_pfx[stance]["metrics"]["pitch_type"]:
                combined_pfx_metrics[stance][0][pitch_type] = {
                    "metrics": career_metrics_by_pitch_type.get(pitch_type, {}),
                }
        all_seasons_played = yearly_pfx["vs_all"]["metrics"].keys()
        for year in list(all_seasons_played):
            combined_pfx_metrics[stance][year] = {}
            if stance in PERCENTILE_SPLITS:
                batter_pfx_percentiles[stance][year]["percentiles"] = yearly_pfx[stance]["percentiles"][year]
            season_metrics_by_pitch_type = yearly_pfx[stance]["metrics"][year]["metrics_by_pitch_type"]
            for pitch_type in all_pitch_types:
                if pitch_type in yearly_pfx[stance]["metrics"][year]["pitch_type"]:
                    combined_pfx_metrics[stance][year][pitch_type] = {
                        "metrics": season_metrics_by_pitch_type.get(pitch_type),
                    }
    return combined_pfx_metrics


def _convert_career_pfx_to_dict(career_pfx):
    for stance in BATTER_STANCE_SPLITS:
        career_pfx[stance]["metrics"] = career_pfx[stance]["metrics"].as_dict()
    return career_pfx


def _convert_yearly_pfx_to_dict(yearly_pfx):
    for stance in BATTER_STANCE_SPLITS:
        for year, pfx_stats_for_year in yearly_pfx[stance]["metrics"].items():
            yearly_pfx[stance]["metrics"][year] = pfx_stats_for_year.as_dict()
    return yearly_pfx


def _get_pitch_types_sorted(metrics_by_pitch_type):
    unsorted = list(metrics_by_pitch_type.values())
    return [str(PitchType(m["pitch_type_int"])) for m in sorted(unsorted, key=lambda x: x["percent"], reverse=True)]
