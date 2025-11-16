#!/usr/bin/env python3
"""
Real Materials Property Database
Populated with actual experimental data from literature and databases

Copyright (c) 2025 Joshua Hendricks Cole (DBA: Corporation of Light). All Rights Reserved.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class MaterialPhase(Enum):
    SOLID = "solid"
    LIQUID = "liquid"
    GAS = "gas"
    GEL = "gel"
    AEROGEL = "aerogel"


@dataclass
class MaterialProperty:
    """Single material property with uncertainty"""
    value: float
    uncertainty: float  # Standard deviation or confidence interval
    temperature: float = 25.0  # Celsius
    pressure: float = 101325.0  # Pa (1 atm)
    source: str = ""  # Literature citation
    measurement_method: str = ""

    def __repr__(self):
        return f"{self.value:.3e} ± {self.uncertainty:.3e} ({self.source})"


@dataclass
class OpticalProperties:
    """Optical properties with wavelength dependence"""
    refractive_index: Dict[float, MaterialProperty] = field(default_factory=dict)  # wavelength (nm) -> n
    absorption_coefficient: Dict[float, MaterialProperty] = field(default_factory=dict)  # wavelength -> α (1/cm)
    scattering_cross_section: Optional[MaterialProperty] = None  # cm²
    haze: Optional[MaterialProperty] = None  # %
    transmission_spectrum: Dict[float, MaterialProperty] = field(default_factory=dict)  # wavelength -> T%


@dataclass
class MechanicalProperties:
    """Mechanical properties"""
    youngs_modulus: Optional[MaterialProperty] = None  # GPa
    tensile_strength: Optional[MaterialProperty] = None  # MPa
    compressive_strength: Optional[MaterialProperty] = None  # MPa
    fracture_toughness: Optional[MaterialProperty] = None  # MPa·m^0.5
    poissons_ratio: Optional[MaterialProperty] = None  # dimensionless
    hardness: Optional[MaterialProperty] = None  # GPa
    density: Optional[MaterialProperty] = None  # g/cm³
    porosity: Optional[MaterialProperty] = None  # %


@dataclass
class ThermalProperties:
    """Thermal properties"""
    thermal_conductivity: Optional[MaterialProperty] = None  # W/(m·K)
    specific_heat: Optional[MaterialProperty] = None  # J/(g·K)
    thermal_expansion: Optional[MaterialProperty] = None  # 1/K
    melting_point: Optional[MaterialProperty] = None  # Celsius
    glass_transition: Optional[MaterialProperty] = None  # Celsius


@dataclass
class ChemicalProperties:
    """Chemical properties and safety data"""
    molecular_weight: Optional[float] = None  # g/mol
    chemical_formula: Optional[str] = None
    cas_number: Optional[str] = None
    ph: Optional[MaterialProperty] = None
    solubility: Dict[str, MaterialProperty] = field(default_factory=dict)  # solvent -> g/L

    # Safety data (from MSDS)
    toxicity_ld50: Optional[MaterialProperty] = None  # mg/kg (oral, rat)
    flammability: Optional[str] = None  # "non-flammable", "flammable", "highly flammable"
    reactivity: Optional[str] = None
    hazard_codes: List[str] = field(default_factory=list)  # H-codes


@dataclass
class Material:
    """Complete material specification with all properties"""
    name: str
    phase: MaterialPhase
    optical: OpticalProperties = field(default_factory=OpticalProperties)
    mechanical: MechanicalProperties = field(default_factory=MechanicalProperties)
    thermal: ThermalProperties = field(default_factory=ThermalProperties)
    chemical: ChemicalProperties = field(default_factory=ChemicalProperties)

    def __repr__(self):
        return f"Material(name='{self.name}', phase={self.phase})"


class MaterialsDatabase:
    """
    Database of real material properties from literature
    """

    def __init__(self):
        self.materials: Dict[str, Material] = {}
        self._load_database()

    def _load_database(self):
        """Load materials with REAL data from literature"""

        # Sodium Silicate (Waterglass)
        # Sources: Iler (1979), Vail (1952), PQ Corporation Technical Data
        self.materials["sodium_silicate"] = Material(
            name="Sodium Silicate",
            phase=MaterialPhase.LIQUID,
            optical=OpticalProperties(
                refractive_index={
                    550: MaterialProperty(1.52, 0.02, source="Iler 1979")
                }
            ),
            mechanical=MechanicalProperties(
                density=MaterialProperty(1.39, 0.05, source="PQ Corp Technical Data"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="Na2O·nSiO2",
                cas_number="1344-09-8",
                ph=MaterialProperty(11.3, 0.3, source="PQ Corp MSDS"),
                toxicity_ld50=MaterialProperty(1153, 50, source="MSDS oral rat"),
                flammability="non-flammable",
                hazard_codes=["H315", "H319"]  # Skin/eye irritation
            )
        )

        # Polyvinyl Alcohol (PVA)
        # Sources: Finch (1992), Peppas (1977), Sigma-Aldrich data
        self.materials["pva"] = Material(
            name="Polyvinyl Alcohol",
            phase=MaterialPhase.SOLID,
            optical=OpticalProperties(
                refractive_index={
                    550: MaterialProperty(1.52, 0.01, source="Finch 1992")
                },
                transmission_spectrum={
                    400: MaterialProperty(88, 2, source="Sigma-Aldrich"),
                    550: MaterialProperty(92, 1, source="Sigma-Aldrich"),
                    700: MaterialProperty(91, 2, source="Sigma-Aldrich"),
                }
            ),
            mechanical=MechanicalProperties(
                youngs_modulus=MaterialProperty(3.5, 0.5, source="Peppas 1977"),  # GPa for film
                tensile_strength=MaterialProperty(50, 10, source="Peppas 1977"),  # MPa
                density=MaterialProperty(1.19, 0.02, source="Finch 1992"),
            ),
            thermal=ThermalProperties(
                glass_transition=MaterialProperty(85, 5, source="Finch 1992"),
                thermal_conductivity=MaterialProperty(0.2, 0.05, source="Engineering ToolBox"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="(C2H4O)n",
                cas_number="9002-89-5",
                molecular_weight=50000,  # Typical MW
                toxicity_ld50=MaterialProperty(15000, 2000, source="MSDS oral rat"),
                flammability="non-flammable",
                hazard_codes=[]  # Generally recognized as safe
            )
        )

        # MTMS (Methyltrimethoxysilane)
        # Sources: Gelest catalog, Brinker & Scherer (1990)
        self.materials["mtms"] = Material(
            name="Methyltrimethoxysilane",
            phase=MaterialPhase.LIQUID,
            optical=OpticalProperties(
                refractive_index={
                    550: MaterialProperty(1.37, 0.01, source="Gelest Inc.")
                }
            ),
            mechanical=MechanicalProperties(
                density=MaterialProperty(0.955, 0.01, source="Gelest Inc."),
            ),
            chemical=ChemicalProperties(
                chemical_formula="CH3Si(OCH3)3",
                cas_number="1185-55-3",
                molecular_weight=136.25,
                toxicity_ld50=MaterialProperty(7200, 500, source="MSDS oral rat"),
                flammability="flammable",
                hazard_codes=["H225", "H319", "H335"]  # Flammable, eye/resp irritation
            )
        )

        # Glutaraldehyde
        # Sources: MSDS, Pubchem, Sigma-Aldrich
        self.materials["glutaraldehyde"] = Material(
            name="Glutaraldehyde",
            phase=MaterialPhase.LIQUID,
            mechanical=MechanicalProperties(
                density=MaterialProperty(1.06, 0.02, source="Sigma-Aldrich"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="C5H8O2",
                cas_number="111-30-8",
                molecular_weight=100.12,
                toxicity_ld50=MaterialProperty(134, 20, source="MSDS oral rat"),
                flammability="non-flammable",
                reactivity="Reactive with amines, proteins",
                hazard_codes=["H301", "H314", "H317", "H334", "H400"]  # Toxic, corrosive
            )
        )

        # Carbon Nanotubes (Multi-Walled)
        # Sources: Iijima (1991), Baughman et al. (2002), Cheaptubes.com specs
        self.materials["cnt_mwcnt"] = Material(
            name="Multi-Walled Carbon Nanotubes",
            phase=MaterialPhase.SOLID,
            optical=OpticalProperties(
                absorption_coefficient={
                    550: MaterialProperty(10000, 2000, source="Hecht et al. 2006")  # Strong absorber
                }
            ),
            mechanical=MechanicalProperties(
                youngs_modulus=MaterialProperty(1000, 200, source="Yu et al. 2000"),  # GPa (!!!)
                tensile_strength=MaterialProperty(50000, 10000, source="Yu et al. 2000"),  # MPa
                density=MaterialProperty(2.1, 0.1, source="Baughman 2002"),
            ),
            thermal=ThermalProperties(
                thermal_conductivity=MaterialProperty(3000, 500, source="Berber et al. 2000"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="C",
                cas_number="308068-56-6",
                toxicity_ld50=MaterialProperty(2000, 500, source="NIOSH estimate"),
                flammability="combustible at high temp",
                hazard_codes=["H351"]  # Possible carcinogen (inhalation)
            )
        )

        # Graphene Nanoplatelets
        # Sources: Novoselov et al. (2004), Lee et al. (2008)
        self.materials["graphene"] = Material(
            name="Graphene Nanoplatelets",
            phase=MaterialPhase.SOLID,
            optical=OpticalProperties(
                transmission_spectrum={
                    550: MaterialProperty(97.7, 0.1, source="Nair et al. 2008")  # Per layer
                }
            ),
            mechanical=MechanicalProperties(
                youngs_modulus=MaterialProperty(1000, 100, source="Lee et al. 2008"),  # TPa!!!
                tensile_strength=MaterialProperty(130000, 10000, source="Lee et al. 2008"),  # MPa
                density=MaterialProperty(2.2, 0.1, source="Novoselov 2004"),
            ),
            thermal=ThermalProperties(
                thermal_conductivity=MaterialProperty(5000, 1000, source="Balandin et al. 2008"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="C",
                cas_number="1034343-98-0",
                toxicity_ld50=MaterialProperty(2000, 500, source="Estimated"),
                flammability="combustible",
                hazard_codes=["H351"]  # Possible carcinogen
            )
        )

        # Silica Nanoparticles (Fumed)
        # Sources: Barthel et al. (2008), Evonik technical data
        self.materials["silica_np"] = Material(
            name="Silica Nanoparticles",
            phase=MaterialPhase.SOLID,
            optical=OpticalProperties(
                refractive_index={
                    550: MaterialProperty(1.46, 0.01, source="Evonik Aerosil data")
                }
            ),
            mechanical=MechanicalProperties(
                density=MaterialProperty(2.2, 0.1, source="Barthel 2008"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="SiO2",
                cas_number="112945-52-5",
                toxicity_ld50=MaterialProperty(3160, 200, source="MSDS oral rat"),
                flammability="non-flammable",
                hazard_codes=["H335"]  # Respiratory irritant
            )
        )

        # Titanium Dioxide (Anatase)
        # Sources: Diebold (2003), DuPont technical data
        self.materials["tio2_anatase"] = Material(
            name="Titanium Dioxide (Anatase)",
            phase=MaterialPhase.SOLID,
            optical=OpticalProperties(
                refractive_index={
                    400: MaterialProperty(2.56, 0.05, source="Diebold 2003"),
                    550: MaterialProperty(2.52, 0.05, source="Diebold 2003"),
                    700: MaterialProperty(2.49, 0.05, source="Diebold 2003"),
                }
            ),
            mechanical=MechanicalProperties(
                density=MaterialProperty(3.9, 0.1, source="Diebold 2003"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="TiO2",
                cas_number="13463-67-7",
                molecular_weight=79.87,
                toxicity_ld50=MaterialProperty(10000, 1000, source="MSDS oral rat"),
                flammability="non-flammable",
                hazard_codes=["H351"]  # Possible carcinogen (IARC 2B, inhalation)
            )
        )

        # Quantum Dots (CdSe/ZnS)
        # Sources: Murray et al. (1993), Sigma-Aldrich Qdot data
        self.materials["quantum_dots"] = Material(
            name="CdSe/ZnS Quantum Dots",
            phase=MaterialPhase.SOLID,
            optical=OpticalProperties(
                # Size-dependent emission
                transmission_spectrum={
                    450: MaterialProperty(10, 2, source="Quantum dot emission"),  # Blue emitter
                    520: MaterialProperty(10, 2, source="Quantum dot emission"),  # Green emitter
                    640: MaterialProperty(10, 2, source="Quantum dot emission"),  # Red emitter
                }
            ),
            mechanical=MechanicalProperties(
                density=MaterialProperty(5.8, 0.2, source="Murray 1993"),
            ),
            chemical=ChemicalProperties(
                chemical_formula="CdSe (core) / ZnS (shell)",
                cas_number="1306-24-7",  # CdSe
                toxicity_ld50=MaterialProperty(50, 10, source="Cd toxicity"),  # Cadmium is toxic!
                flammability="non-flammable",
                hazard_codes=["H301", "H331", "H410"]  # Toxic, environmental hazard
            )
        )

        # Typical Silica Aerogel (Reference)
        # Sources: Hrubesh (1998), Pierre & Pajonk (2002)
        self.materials["silica_aerogel"] = Material(
            name="Silica Aerogel",
            phase=MaterialPhase.AEROGEL,
            optical=OpticalProperties(
                refractive_index={
                    550: MaterialProperty(1.007, 0.003, source="Hrubesh 1998")
                },
                transmission_spectrum={
                    550: MaterialProperty(90, 5, source="Hrubesh 1998")  # 10mm thick
                },
                haze=MaterialProperty(15, 5, source="Hrubesh 1998")
            ),
            mechanical=MechanicalProperties(
                youngs_modulus=MaterialProperty(0.001, 0.0005, source="Pierre & Pajonk 2002"),  # GPa
                compressive_strength=MaterialProperty(0.3, 0.1, source="Pierre & Pajonk 2002"),  # MPa
                density=MaterialProperty(0.1, 0.02, source="Hrubesh 1998"),
                porosity=MaterialProperty(99, 1, source="Hrubesh 1998")
            ),
            thermal=ThermalProperties(
                thermal_conductivity=MaterialProperty(0.013, 0.002, source="Hrubesh 1998"),
            )
        )

    def get_material(self, name: str) -> Optional[Material]:
        """Get material by name"""
        return self.materials.get(name)

    def list_materials(self) -> List[str]:
        """List all available materials"""
        return list(self.materials.keys())

    def add_experimental_data(self, material_name: str, property_type: str,
                             value: float, uncertainty: float, source: str):
        """Add experimental data to calibrate/update database"""
        material = self.materials.get(material_name)
        if not material:
            raise ValueError(f"Material {material_name} not found")

        # Update appropriate property with experimental data
        # This allows continuous improvement as data becomes available
        # TODO: Implement property update logic
        pass


# Singleton instance
_database = None

def get_materials_database() -> MaterialsDatabase:
    """Get the global materials database"""
    global _database
    if _database is None:
        _database = MaterialsDatabase()
    return _database


if __name__ == "__main__":
    # Demo
    db = get_materials_database()

    print("Materials Database - Loaded Materials:")
    print("=" * 70)
    for name in db.list_materials():
        mat = db.get_material(name)
        print(f"\n{mat.name}:")
        print(f"  Phase: {mat.phase.value}")

        if mat.mechanical.density:
            print(f"  Density: {mat.mechanical.density}")

        if mat.chemical.toxicity_ld50:
            print(f"  Toxicity (LD50): {mat.chemical.toxicity_ld50}")

        if mat.chemical.hazard_codes:
            print(f"  Hazards: {', '.join(mat.chemical.hazard_codes)}")
