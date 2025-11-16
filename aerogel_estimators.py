#!/usr/bin/env python3
"""
Shared analytic estimators for the ECH0 aerogel recipes.

Each recipe is described by a small set of parameters (freeze temperature, PVA
ratio, MTMS loading, glutaraldehyde cross-linker, and optional nano-additives).
The functions in this module convert those knobs into deterministic estimates of
mean pore size, transparency, and structural integrity so that the workflow can
be reproduced without invoking unverifiable "quantum" tooling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple


ADDITIVE_EFFECTS = {
    "cnt": {"pore": 0.0012, "transparency": 0.22, "structure": 2.4},
    "graphene": {"pore": 0.0014, "transparency": 0.28, "structure": 2.1},
    "silica_np": {"pore": 0.0010, "transparency": 0.18, "structure": 1.1},
    "tio2": {"pore": 0.0006, "transparency": -0.25, "structure": 0.9},
    "mof": {"pore": 0.0008, "transparency": 0.05, "structure": 0.6},
    "quantum_dots": {"pore": -0.0005, "transparency": -0.6, "structure": 0.2},
}


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


@dataclass(frozen=True)
class AerogelRecipe:
    name: str
    freeze_temp_c: float
    base_material: str
    pva_mass_fraction: float  # e.g. 0.25 for 1:4 ratio
    mtms_wt_percent: float
    glutaraldehyde_vol_percent: float
    additives: Dict[str, float] = field(default_factory=dict)
    drying_method: str = "freeze_dry"  # or "supercritical"
    target_transparency: float = 90.0
    baseline_pore_nm: float = 50.0


def compute_temperature_ratio(recipe: AerogelRecipe) -> float:
    return _clamp(abs(recipe.freeze_temp_c) / 78.0, 0.2, 1.5)


def estimate_pore_stats(recipe: AerogelRecipe) -> Dict[str, float]:
    ratio = compute_temperature_ratio(recipe)
    ice_crystal_nm = recipe.baseline_pore_nm / ratio

    pva_pct = recipe.pva_mass_fraction * 100.0
    mean_nm = ice_crystal_nm
    mean_nm *= 1.0 - 0.0030 * pva_pct
    mean_nm *= 1.0 - 0.0017 * recipe.mtms_wt_percent
    mean_nm *= 1.0 - 0.0013 * recipe.glutaraldehyde_vol_percent

    for additive, load in recipe.additives.items():
        effect = ADDITIVE_EFFECTS.get(additive)
        if not effect:
            continue
        mean_nm *= 1.0 - effect["pore"] * load

    if recipe.drying_method == "supercritical":
        mean_nm *= 0.97  # finer pores due to reduced capillary stress

    std_nm = mean_nm * 0.25
    return {
        "mean": mean_nm,
        "std": std_nm,
        "min": max(1.0, mean_nm - 2.0 * std_nm),
        "max": mean_nm + 2.0 * std_nm,
    }


def estimate_transparency(recipe: AerogelRecipe, pore_stats: Dict[str, float]) -> float:
    mean_nm = pore_stats["mean"]
    scattering = (mean_nm / 550.0) ** 4
    transparency = 98.0 - 100.0 * scattering

    pva_pct = recipe.pva_mass_fraction * 100.0
    transparency += 0.08 * pva_pct
    transparency += 0.35 * recipe.mtms_wt_percent
    transparency += 0.75 * recipe.glutaraldehyde_vol_percent

    for additive, load in recipe.additives.items():
        effect = ADDITIVE_EFFECTS.get(additive)
        if effect:
            transparency += effect["transparency"] * load

    if recipe.base_material.lower() == "sodium_silicate":
        transparency -= 8.0
    elif recipe.base_material.lower() == "teos":
        transparency -= 2.0

    if recipe.drying_method == "supercritical":
        transparency += 1.5

    return _clamp(transparency, 0.0, 100.0)


def estimate_structural(
    recipe: AerogelRecipe,
) -> Tuple[float, Dict[str, float]]:
    pva_contrib = recipe.pva_mass_fraction * 12.0
    crosslink_contrib = recipe.mtms_wt_percent / 5.0
    glutaraldehyde_contrib = recipe.glutaraldehyde_vol_percent * 1.4

    additive_bonus = 0.0
    for additive, load in recipe.additives.items():
        effect = ADDITIVE_EFFECTS.get(additive)
        if effect:
            additive_bonus += effect["structure"] * load

    base_sum = pva_contrib + crosslink_contrib + glutaraldehyde_contrib + additive_bonus

    thermal_factor = 0.6 + 0.4 * _clamp(compute_temperature_ratio(recipe), 0.2, 1.0)
    if recipe.drying_method == "supercritical":
        thermal_factor += 0.1

    structural_score = base_sum * thermal_factor

    if structural_score >= 8.0:
        rating = "excellent"
    elif structural_score >= 5.0:
        rating = "good"
    elif structural_score >= 3.0:
        rating = "fair"
    else:
        rating = "poor"

    return structural_score, {
        "polymer": pva_contrib,
        "crosslink": crosslink_contrib,
        "glutaraldehyde": glutaraldehyde_contrib,
        "additive_bonus": additive_bonus,
        "thermal_factor": thermal_factor,
        "rating": rating,
    }


def evaluate_recipe(recipe: AerogelRecipe) -> Dict[str, object]:
    pore_stats = estimate_pore_stats(recipe)
    transparency = estimate_transparency(recipe, pore_stats)
    structural_score, structural_breakdown = estimate_structural(recipe)

    meets_transparency = transparency >= recipe.target_transparency
    meets_structure = structural_score >= 5.0

    if meets_transparency and meets_structure:
        verdict = "viable"
    elif meets_transparency or structural_score >= 3.0:
        verdict = "requires_modification"
    else:
        verdict = "not_viable"

    return {
        "recipe": recipe,
        "pore_stats": pore_stats,
        "transparency_percent": transparency,
        "meets_transparency_target": bool(meets_transparency),
        "structural_score": structural_score,
        "structural_breakdown": structural_breakdown,
        "verdict": verdict,
    }


def format_console_report(
    evaluation: Dict[str, object],
    lines: Iterable[str] | None = None,
) -> str:
    recipe: AerogelRecipe = evaluation["recipe"]
    pore_stats = evaluation["pore_stats"]
    transparency = evaluation["transparency_percent"]
    structural_score = evaluation["structural_score"]
    structural_breakdown = evaluation["structural_breakdown"]

    output_lines = list(lines or [])
    output_lines.append(f"Recipe: {recipe.name}")
    output_lines.append("-" * (8 + len(recipe.name)))
    output_lines.append(f"Freeze temp            : {recipe.freeze_temp_c:.1f} °C")
    output_lines.append(f"PVA mass fraction      : {recipe.pva_mass_fraction:.3f}")
    output_lines.append(f"MTMS (wt %)            : {recipe.mtms_wt_percent:.2f}")
    output_lines.append(f"Glutaraldehyde (vol %) : {recipe.glutaraldehyde_vol_percent:.2f}")
    if recipe.additives:
        output_lines.append("Additives (wt % unless noted):")
        for name, load in recipe.additives.items():
            output_lines.append(f"  - {name}: {load}")
    else:
        output_lines.append("Additives              : none")
    output_lines.append("")

    output_lines.append("Pore statistics (nm):")
    output_lines.append(f"  mean = {pore_stats['mean']:.1f}")
    output_lines.append(f"  std  = {pore_stats['std']:.1f}")
    output_lines.append(f"  min  = {pore_stats['min']:.1f}")
    output_lines.append(f"  max  = {pore_stats['max']:.1f}")
    output_lines.append("")

    output_lines.append(f"Estimated transparency : {transparency:.1f}%")
    output_lines.append(
        f"Meets target ({recipe.target_transparency:.1f}%): "
        f"{evaluation['meets_transparency_target']}"
    )
    output_lines.append("")

    output_lines.append(f"Structural score       : {structural_score:.2f} / 10")
    output_lines.append(f"Rating                 : {structural_breakdown['rating']}")
    output_lines.append(
        "Breakdown              : "
        f"polymer={structural_breakdown['polymer']:.2f}, "
        f"crosslink={structural_breakdown['crosslink']:.2f}, "
        f"glutaraldehyde={structural_breakdown['glutaraldehyde']:.2f}, "
        f"additives={structural_breakdown['additive_bonus']:.2f}, "
        f"thermal_factor={structural_breakdown['thermal_factor']:.2f}"
    )
    output_lines.append("")
    output_lines.append(f"Verdict                : {evaluation['verdict']}")

    return "\n".join(output_lines)
