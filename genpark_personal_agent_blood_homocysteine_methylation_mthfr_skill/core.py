# -*- coding: utf-8 -*-
"""Blood Homocysteine Methylation Sentinel for GenPark Personal Agent."""
import json
from typing import Dict, Any

class BloodHomocysteineMethylationSentinel:
    @staticmethod
    def stratify_homocysteine_cardiovascular_risk(homocysteine_umol_l: float, mthfr_genotype: str = "wild_type_CC") -> Dict[str, Any]:
        # Optimal longevity range: 6.0 - 8.5 umol/L
        if homocysteine_umol_l > 15.0:
            tier = "SEVERE_HYPERHOMOCYSTEINEMIA"
            cv_risk_mult = 2.4
            pathology = "High endothelial vascular inflammation, carotid intima-media thickening, and neurodegenerative amyloid vulnerability."
        elif homocysteine_umol_l > 10.0:
            tier = "MODERATE_ELEVATION_SUBOPTIMAL"
            cv_risk_mult = 1.6
            pathology = "Suboptimal methylation recycling; elevated oxidative stress in arterial walls."
        elif homocysteine_umol_l >= 6.0:
            tier = "OPTIMAL_LONGEVITY_RANGE"
            cv_risk_mult = 1.0
            pathology = "Balanced transsulfuration and remethylation fluxes."
        else:
            tier = "LOW_HOMOCYSTEINE_DEPLETION"
            cv_risk_mult = 1.1
            pathology = "Potential glutathione synthesis bottleneck due to low transsulfuration substrate."

        mthfr_penalty = 1.3 if mthfr_genotype in ["homozygous_TT", "compound_heterozygous"] else 1.0
        return {
            "plasma_homocysteine_umol_l": homocysteine_umol_l,
            "mthfr_genotype": mthfr_genotype,
            "methylation_tier": tier,
            "relative_cardiovascular_hazard": round(cv_risk_mult * mthfr_penalty, 2),
            "clinical_pathophysiology": pathology
        }

    @staticmethod
    def prescribe_methyl_donor_repletion_protocol(baseline_homocysteine: float, target_homocysteine: float = 7.5) -> Dict[str, Any]:
        spread = max(0.0, baseline_homocysteine - target_homocysteine)
        folate_dose_mcg = min(3000, max(400, int(spread * 250)))
        tmg_dose_mg = 1500 if spread > 5.0 else 500
        return {
            "target_homocysteine_umol_l": target_homocysteine,
            "expected_reduction_window_weeks": 8,
            "prescribed_repletion": [
                f"L-Methylfolate (5-MTHF): {folate_dose_mcg} mcg daily with breakfast",
                "Methylcobalamin (Bioactive B12): 1,000 mcg sublingual daily",
                f"Trimethylglycine (Betaine TMG): {tmg_dose_mg} mg to fuel BHMT liver remethylation bypass",
                "Pyridoxal-5-Phosphate (Active B6): 50 mg to support cystathionine beta-synthase transsulfuration"
            ],
            "dietary_guidelines": "Incorporate steamed pasture eggs (choline) and dark leafy spinach daily."
        }
