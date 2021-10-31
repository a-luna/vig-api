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
    career_pfx = _convert_career_pfx_to_dict(career_pfx)
    yearly_pfx = _convert_yearly_pfx_to_dict(yearly_pfx)
    for stance in PERCENTILE_SPLITS:
        combined_pfx_metrics[stance] = {
            0: {
                "metrics": career_pfx[stance]["metrics"]["metrics_combined"],
                "percentiles": career_pfx[stance]["percentiles"],
            }
        }
        for year in list(yearly_pfx["vs_all"]["metrics"].keys()):
            combined_pfx_metrics[stance][year] = {
                "metrics": yearly_pfx[stance]["metrics"][year]["metrics_combined"],
                "percentiles": yearly_pfx[stance]["percentiles"][year],
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
