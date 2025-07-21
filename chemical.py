import tkinter as tk
from tkinter import messagebox

# --- Data for Periodic Table (full table) ---
ELEMENTS = [
    {"symbol": "H",  "name": "Hydrogen",      "atomic_number": 1,  "atomic_weight": 1.008,    "group": 1,  "period": 1, "col": 0,  "row": 0},
    {"symbol": "He", "name": "Helium",        "atomic_number": 2,  "atomic_weight": 4.0026,   "group": 18, "period": 1, "col": 17, "row": 0},
    {"symbol": "Li", "name": "Lithium",       "atomic_number": 3,  "atomic_weight": 6.94,     "group": 1,  "period": 2, "col": 0,  "row": 1},
    {"symbol": "Be", "name": "Beryllium",     "atomic_number": 4,  "atomic_weight": 9.0122,   "group": 2,  "period": 2, "col": 1,  "row": 1},
    {"symbol": "B",  "name": "Boron",         "atomic_number": 5,  "atomic_weight": 10.81,    "group": 13, "period": 2, "col": 12, "row": 1},
    {"symbol": "C",  "name": "Carbon",        "atomic_number": 6,  "atomic_weight": 12.011,   "group": 14, "period": 2, "col": 13, "row": 1},
    {"symbol": "N",  "name": "Nitrogen",      "atomic_number": 7,  "atomic_weight": 14.007,   "group": 15, "period": 2, "col": 14, "row": 1},
    {"symbol": "O",  "name": "Oxygen",        "atomic_number": 8,  "atomic_weight": 15.999,   "group": 16, "period": 2, "col": 15, "row": 1},
    {"symbol": "F",  "name": "Fluorine",      "atomic_number": 9,  "atomic_weight": 18.998,   "group": 17, "period": 2, "col": 16, "row": 1},
    {"symbol": "Ne", "name": "Neon",          "atomic_number": 10, "atomic_weight": 20.180,   "group": 18, "period": 2, "col": 17, "row": 1},
    {"symbol": "Na", "name": "Sodium",        "atomic_number": 11, "atomic_weight": 22.990,   "group": 1,  "period": 3, "col": 0,  "row": 2},
    {"symbol": "Mg", "name": "Magnesium",     "atomic_number": 12, "atomic_weight": 24.305,   "group": 2,  "period": 3, "col": 1,  "row": 2},
    {"symbol": "Al", "name": "Aluminum",      "atomic_number": 13, "atomic_weight": 26.982,   "group": 13, "period": 3, "col": 12, "row": 2},
    {"symbol": "Si", "name": "Silicon",       "atomic_number": 14, "atomic_weight": 28.085,   "group": 14, "period": 3, "col": 13, "row": 2},
    {"symbol": "P",  "name": "Phosphorus",    "atomic_number": 15, "atomic_weight": 30.974,   "group": 15, "period": 3, "col": 14, "row": 2},
    {"symbol": "S",  "name": "Sulfur",        "atomic_number": 16, "atomic_weight": 32.06,    "group": 16, "period": 3, "col": 15, "row": 2},
    {"symbol": "Cl", "name": "Chlorine",      "atomic_number": 17, "atomic_weight": 35.45,    "group": 17, "period": 3, "col": 16, "row": 2},
    {"symbol": "Ar", "name": "Argon",         "atomic_number": 18, "atomic_weight": 39.948,   "group": 18, "period": 3, "col": 17, "row": 2},
    {"symbol": "K",  "name": "Potassium",     "atomic_number": 19, "atomic_weight": 39.098,   "group": 1,  "period": 4, "col": 0,  "row": 3},
    {"symbol": "Ca", "name": "Calcium",       "atomic_number": 20, "atomic_weight": 40.078,   "group": 2,  "period": 4, "col": 1,  "row": 3},
    {"symbol": "Sc", "name": "Scandium",      "atomic_number": 21, "atomic_weight": 44.956,   "group": 3,  "period": 4, "col": 2,  "row": 3},
    {"symbol": "Ti", "name": "Titanium",      "atomic_number": 22, "atomic_weight": 47.867,   "group": 4,  "period": 4, "col": 3,  "row": 3},
    {"symbol": "V",  "name": "Vanadium",      "atomic_number": 23, "atomic_weight": 50.942,   "group": 5,  "period": 4, "col": 4,  "row": 3},
    {"symbol": "Cr", "name": "Chromium",      "atomic_number": 24, "atomic_weight": 51.996,   "group": 6,  "period": 4, "col": 5,  "row": 3},
    {"symbol": "Mn", "name": "Manganese",     "atomic_number": 25, "atomic_weight": 54.938,   "group": 7,  "period": 4, "col": 6,  "row": 3},
    {"symbol": "Fe", "name": "Iron",          "atomic_number": 26, "atomic_weight": 55.845,   "group": 8,  "period": 4, "col": 7,  "row": 3},
    {"symbol": "Co", "name": "Cobalt",        "atomic_number": 27, "atomic_weight": 58.933,   "group": 9,  "period": 4, "col": 8,  "row": 3},
    {"symbol": "Ni", "name": "Nickel",        "atomic_number": 28, "atomic_weight": 58.693,   "group": 10, "period": 4, "col": 9,  "row": 3},
    {"symbol": "Cu", "name": "Copper",        "atomic_number": 29, "atomic_weight": 63.546,   "group": 11, "period": 4, "col": 10, "row": 3},
    {"symbol": "Zn", "name": "Zinc",          "atomic_number": 30, "atomic_weight": 65.38,    "group": 12, "period": 4, "col": 11, "row": 3},
    {"symbol": "Ga", "name": "Gallium",       "atomic_number": 31, "atomic_weight": 69.723,   "group": 13, "period": 4, "col": 12, "row": 3},
    {"symbol": "Ge", "name": "Germanium",     "atomic_number": 32, "atomic_weight": 72.630,   "group": 14, "period": 4, "col": 13, "row": 3},
    {"symbol": "As", "name": "Arsenic",       "atomic_number": 33, "atomic_weight": 74.922,   "group": 15, "period": 4, "col": 14, "row": 3},
    {"symbol": "Se", "name": "Selenium",      "atomic_number": 34, "atomic_weight": 78.971,   "group": 16, "period": 4, "col": 15, "row": 3},
    {"symbol": "Br", "name": "Bromine",       "atomic_number": 35, "atomic_weight": 79.904,   "group": 17, "period": 4, "col": 16, "row": 3},
    {"symbol": "Kr", "name": "Krypton",       "atomic_number": 36, "atomic_weight": 83.798,   "group": 18, "period": 4, "col": 17, "row": 3},
    {"symbol": "Rb", "name": "Rubidium",      "atomic_number": 37, "atomic_weight": 85.468,   "group": 1,  "period": 5, "col": 0,  "row": 4},
    {"symbol": "Sr", "name": "Strontium",     "atomic_number": 38, "atomic_weight": 87.62,    "group": 2,  "period": 5, "col": 1,  "row": 4},
    {"symbol": "Y",  "name": "Yttrium",       "atomic_number": 39, "atomic_weight": 88.906,   "group": 3,  "period": 5, "col": 2,  "row": 4},
    {"symbol": "Zr", "name": "Zirconium",     "atomic_number": 40, "atomic_weight": 91.224,   "group": 4,  "period": 5, "col": 3,  "row": 4},
    {"symbol": "Nb", "name": "Niobium",       "atomic_number": 41, "atomic_weight": 92.906,   "group": 5,  "period": 5, "col": 4,  "row": 4},
    {"symbol": "Mo", "name": "Molybdenum",    "atomic_number": 42, "atomic_weight": 95.95,    "group": 6,  "period": 5, "col": 5,  "row": 4},
    {"symbol": "Tc", "name": "Technetium",    "atomic_number": 43, "atomic_weight": 98,       "group": 7,  "period": 5, "col": 6,  "row": 4},
    {"symbol": "Ru", "name": "Ruthenium",     "atomic_number": 44, "atomic_weight": 101.07,   "group": 8,  "period": 5, "col": 7,  "row": 4},
    {"symbol": "Rh", "name": "Rhodium",       "atomic_number": 45, "atomic_weight": 102.91,   "group": 9,  "period": 5, "col": 8,  "row": 4},
    {"symbol": "Pd", "name": "Palladium",     "atomic_number": 46, "atomic_weight": 106.42,   "group": 10, "period": 5, "col": 9,  "row": 4},
    {"symbol": "Ag", "name": "Silver",        "atomic_number": 47, "atomic_weight": 107.87,   "group": 11, "period": 5, "col": 10, "row": 4},
    {"symbol": "Cd", "name": "Cadmium",       "atomic_number": 48, "atomic_weight": 112.41,   "group": 12, "period": 5, "col": 11, "row": 4},
    {"symbol": "In", "name": "Indium",        "atomic_number": 49, "atomic_weight": 114.82,   "group": 13, "period": 5, "col": 12, "row": 4},
    {"symbol": "Sn", "name": "Tin",           "atomic_number": 50, "atomic_weight": 118.71,   "group": 14, "period": 5, "col": 13, "row": 4},
    {"symbol": "Sb", "name": "Antimony",      "atomic_number": 51, "atomic_weight": 121.76,   "group": 15, "period": 5, "col": 14, "row": 4},
    {"symbol": "Te", "name": "Tellurium",     "atomic_number": 52, "atomic_weight": 127.60,   "group": 16, "period": 5, "col": 15, "row": 4},
    {"symbol": "I",  "name": "Iodine",        "atomic_number": 53, "atomic_weight": 126.90,   "group": 17, "period": 5, "col": 16, "row": 4},
    {"symbol": "Xe", "name": "Xenon",         "atomic_number": 54, "atomic_weight": 131.29,   "group": 18, "period": 5, "col": 17, "row": 4},
    {"symbol": "Cs", "name": "Cesium",        "atomic_number": 55, "atomic_weight": 132.91,   "group": 1,  "period": 6, "col": 0,  "row": 5},
    {"symbol": "Ba", "name": "Barium",        "atomic_number": 56, "atomic_weight": 137.33,   "group": 2,  "period": 6, "col": 1,  "row": 5},
    {"symbol": "La", "name": "Lanthanum",     "atomic_number": 57, "atomic_weight": 138.91,   "group": 3,  "period": 6, "col": 2,  "row": 8},  # Lanthanide
    {"symbol": "Ce", "name": "Cerium",        "atomic_number": 58, "atomic_weight": 140.12,   "group": None, "period": 6, "col": 3,  "row": 8},
    {"symbol": "Pr", "name": "Praseodymium",  "atomic_number": 59, "atomic_weight": 140.91,   "group": None, "period": 6, "col": 4,  "row": 8},
    {"symbol": "Nd", "name": "Neodymium",     "atomic_number": 60, "atomic_weight": 144.24,   "group": None, "period": 6, "col": 5,  "row": 8},
    {"symbol": "Pm", "name": "Promethium",    "atomic_number": 61, "atomic_weight": 145,      "group": None, "period": 6, "col": 6,  "row": 8},
    {"symbol": "Sm", "name": "Samarium",      "atomic_number": 62, "atomic_weight": 150.36,   "group": None, "period": 6, "col": 7,  "row": 8},
    {"symbol": "Eu", "name": "Europium",      "atomic_number": 63, "atomic_weight": 151.96,   "group": None, "period": 6, "col": 8,  "row": 8},
    {"symbol": "Gd", "name": "Gadolinium",    "atomic_number": 64, "atomic_weight": 157.25,   "group": None, "period": 6, "col": 9,  "row": 8},
    {"symbol": "Tb", "name": "Terbium",       "atomic_number": 65, "atomic_weight": 158.93,   "group": None, "period": 6, "col": 10, "row": 8},
    {"symbol": "Dy", "name": "Dysprosium",    "atomic_number": 66, "atomic_weight": 162.50,   "group": None, "period": 6, "col": 11, "row": 8},
    {"symbol": "Ho", "name": "Holmium",       "atomic_number": 67, "atomic_weight": 164.93,   "group": None, "period": 6, "col": 12, "row": 8},
    {"symbol": "Er", "name": "Erbium",        "atomic_number": 68, "atomic_weight": 167.26,   "group": None, "period": 6, "col": 13, "row": 8},
    {"symbol": "Tm", "name": "Thulium",       "atomic_number": 69, "atomic_weight": 168.93,   "group": None, "period": 6, "col": 14, "row": 8},
    {"symbol": "Yb", "name": "Ytterbium",     "atomic_number": 70, "atomic_weight": 173.05,   "group": None, "period": 6, "col": 15, "row": 8},
    {"symbol": "Lu", "name": "Lutetium",      "atomic_number": 71, "atomic_weight": 174.97,   "group": 3,  "period": 6, "col": 16, "row": 8},
    {"symbol": "Hf", "name": "Hafnium",       "atomic_number": 72, "atomic_weight": 178.49,   "group": 4,  "period": 6, "col": 3,  "row": 5},
    {"symbol": "Ta", "name": "Tantalum",      "atomic_number": 73, "atomic_weight": 180.95,   "group": 5,  "period": 6, "col": 4,  "row": 5},
    {"symbol": "W",  "name": "Tungsten",      "atomic_number": 74, "atomic_weight": 183.84,   "group": 6,  "period": 6, "col": 5,  "row": 5},
    {"symbol": "Re", "name": "Rhenium",       "atomic_number": 75, "atomic_weight": 186.21,   "group": 7,  "period": 6, "col": 6,  "row": 5},
    {"symbol": "Os", "name": "Osmium",        "atomic_number": 76, "atomic_weight": 190.23,   "group": 8,  "period": 6, "col": 7,  "row": 5},
    {"symbol": "Ir", "name": "Iridium",       "atomic_number": 77, "atomic_weight": 192.22,   "group": 9,  "period": 6, "col": 8,  "row": 5},
    {"symbol": "Pt", "name": "Platinum",      "atomic_number": 78, "atomic_weight": 195.08,   "group": 10, "period": 6, "col": 9,  "row": 5},
    {"symbol": "Au", "name": "Gold",          "atomic_number": 79, "atomic_weight": 196.97,   "group": 11, "period": 6, "col": 10, "row": 5},
    {"symbol": "Hg", "name": "Mercury",       "atomic_number": 80, "atomic_weight": 200.59,   "group": 12, "period": 6, "col": 11, "row": 5},
    {"symbol": "Tl", "name": "Thallium",      "atomic_number": 81, "atomic_weight": 204.38,   "group": 13, "period": 6, "col": 12, "row": 5},
    {"symbol": "Pb", "name": "Lead",          "atomic_number": 82, "atomic_weight": 207.2,    "group": 14, "period": 6, "col": 13, "row": 5},
    {"symbol": "Bi", "name": "Bismuth",       "atomic_number": 83, "atomic_weight": 208.98,   "group": 15, "period": 6, "col": 14, "row": 5},
    {"symbol": "Po", "name": "Polonium",      "atomic_number": 84, "atomic_weight": 209,      "group": 16, "period": 6, "col": 15, "row": 5},
    {"symbol": "At", "name": "Astatine",      "atomic_number": 85, "atomic_weight": 210,      "group": 17, "period": 6, "col": 16, "row": 5},
    {"symbol": "Rn", "name": "Radon",         "atomic_number": 86, "atomic_weight": 222,      "group": 18, "period": 6, "col": 17, "row": 5},
    {"symbol": "Fr", "name": "Francium",      "atomic_number": 87, "atomic_weight": 223,      "group": 1,  "period": 7, "col": 0,  "row": 6},
    {"symbol": "Ra", "name": "Radium",        "atomic_number": 88, "atomic_weight": 226,      "group": 2,  "period": 7, "col": 1,  "row": 6},
    {"symbol": "Ac", "name": "Actinium",      "atomic_number": 89, "atomic_weight": 227,      "group": 3,  "period": 7, "col": 2,  "row": 9},  # Actinide
    {"symbol": "Th", "name": "Thorium",       "atomic_number": 90, "atomic_weight": 232.04,   "group": None, "period": 7, "col": 3,  "row": 9},
    {"symbol": "Pa", "name": "Protactinium",  "atomic_number": 91, "atomic_weight": 231.04,   "group": None, "period": 7, "col": 4,  "row": 9},
    {"symbol": "U",  "name": "Uranium",       "atomic_number": 92, "atomic_weight": 238.03,   "group": None, "period": 7, "col": 5,  "row": 9},
    {"symbol": "Np", "name": "Neptunium",     "atomic_number": 93, "atomic_weight": 237,      "group": None, "period": 7, "col": 6,  "row": 9},
    {"symbol": "Pu", "name": "Plutonium",     "atomic_number": 94, "atomic_weight": 244,      "group": None, "period": 7, "col": 7,  "row": 9},
    {"symbol": "Am", "name": "Americium",     "atomic_number": 95, "atomic_weight": 243,      "group": None, "period": 7, "col": 8,  "row": 9},
    {"symbol": "Cm", "name": "Curium",        "atomic_number": 96, "atomic_weight": 247,      "group": None, "period": 7, "col": 9,  "row": 9},
    {"symbol": "Bk", "name": "Berkelium",     "atomic_number": 97, "atomic_weight": 247,      "group": None, "period": 7, "col": 10, "row": 9},
    {"symbol": "Cf", "name": "Californium",   "atomic_number": 98, "atomic_weight": 251,      "group": None, "period": 7, "col": 11, "row": 9},
    {"symbol": "Es", "name": "Einsteinium",   "atomic_number": 99, "atomic_weight": 252,      "group": None, "period": 7, "col": 12, "row": 9},
    {"symbol": "Fm", "name": "Fermium",       "atomic_number": 100,"atomic_weight": 257,      "group": None, "period": 7, "col": 13, "row": 9},
    {"symbol": "Md", "name": "Mendelevium",   "atomic_number": 101,"atomic_weight": 258,      "group": None, "period": 7, "col": 14, "row": 9},
    {"symbol": "No", "name": "Nobelium",      "atomic_number": 102,"atomic_weight": 259,      "group": None, "period": 7, "col": 15, "row": 9},
    {"symbol": "Lr", "name": "Lawrencium",    "atomic_number": 103,"atomic_weight": 266,      "group": 3,  "period": 7, "col": 16, "row": 9},
    {"symbol": "Rf", "name": "Rutherfordium", "atomic_number": 104,"atomic_weight": 267,      "group": 4,  "period": 7, "col": 3,  "row": 6},
    {"symbol": "Db", "name": "Dubnium",       "atomic_number": 105,"atomic_weight": 270,      "group": 5,  "period": 7, "col": 4,  "row": 6},
    {"symbol": "Sg", "name": "Seaborgium",    "atomic_number": 106,"atomic_weight": 271,      "group": 6,  "period": 7, "col": 5,  "row": 6},
    {"symbol": "Bh", "name": "Bohrium",       "atomic_number": 107,"atomic_weight": 270,      "group": 7,  "period": 7, "col": 6,  "row": 6},
    {"symbol": "Hs", "name": "Hassium",       "atomic_number": 108,"atomic_weight": 277,      "group": 8,  "period": 7, "col": 7,  "row": 6},
    {"symbol": "Mt", "name": "Meitnerium",    "atomic_number": 109,"atomic_weight": 278,      "group": 9,  "period": 7, "col": 8,  "row": 6},
    {"symbol": "Ds", "name": "Darmstadtium",  "atomic_number": 110,"atomic_weight": 281,      "group": 10, "period": 7, "col": 9,  "row": 6},
    {"symbol": "Rg", "name": "Roentgenium",   "atomic_number": 111,"atomic_weight": 282,      "group": 11, "period": 7, "col": 10, "row": 6},
    {"symbol": "H", "name": "Hydrogen", "atomic_number": 1, "atomic_weight": 1.008, "group": 1, "period": 1, "col": 0, "row": 0},
    {"symbol": "He", "name": "Helium", "atomic_number": 2, "atomic_weight": 4.0026, "group": 18, "period": 1, "col": 17, "row": 0},
    {"symbol": "Li", "name": "Lithium", "atomic_number": 3, "atomic_weight": 6.94, "group": 1, "period": 2, "col": 0, "row": 1},
    {"symbol": "Be", "name": "Beryllium", "atomic_number": 4, "atomic_weight": 9.0122, "group": 2, "period": 2, "col": 1, "row": 1},
    {"symbol": "B", "name": "Boron", "atomic_number": 5, "atomic_weight": 10.81, "group": 13, "period": 2, "col": 12, "row": 1},
    {"symbol": "C", "name": "Carbon", "atomic_number": 6, "atomic_weight": 12.011, "group": 14, "period": 2, "col": 13, "row": 1},
    {"symbol": "N", "name": "Nitrogen", "atomic_number": 7, "atomic_weight": 14.007, "group": 15, "period": 2, "col": 14, "row": 1},
    {"symbol": "O", "name": "Oxygen", "atomic_number": 8, "atomic_weight": 15.999, "group": 16, "period": 2, "col": 15, "row": 1},
    {"symbol": "F", "name": "Fluorine", "atomic_number": 9, "atomic_weight": 18.998, "group": 17, "period": 2, "col": 16, "row": 1},
    {"symbol": "Ne", "name": "Neon", "atomic_number": 10, "atomic_weight": 20.180, "group": 18, "period": 2, "col": 17, "row": 1},
    {"symbol": "Na", "name": "Sodium", "atomic_number": 11, "atomic_weight": 22.990, "group": 1, "period": 3, "col": 0, "row": 2},
    {"symbol": "Mg", "name": "Magnesium", "atomic_number": 12, "atomic_weight": 24.305, "group": 2, "period": 3, "col": 1, "row": 2},
    {"symbol": "Al", "name": "Aluminum", "atomic_number": 13, "atomic_weight": 26.982, "group": 13, "period": 3, "col": 12, "row": 2},
    {"symbol": "Si", "name": "Silicon", "atomic_number": 14, "atomic_weight": 28.085, "group": 14, "period": 3, "col": 13, "row": 2},
    {"symbol": "P", "name": "Phosphorus", "atomic_number": 15, "atomic_weight": 30.974, "group": 15, "period": 3, "col": 14, "row": 2},
    {"symbol": "S", "name": "Sulfur", "atomic_number": 16, "atomic_weight": 32.06, "group": 16, "period": 3, "col": 15, "row": 2},
    {"symbol": "Cl", "name": "Chlorine", "atomic_number": 17, "atomic_weight": 35.45, "group": 17, "period": 3, "col": 16, "row": 2},
    {"symbol": "Ar", "name": "Argon", "atomic_number": 18, "atomic_weight": 39.948, "group": 18, "period": 3, "col": 17, "row": 2},
    {"symbol": "K", "name": "Potassium", "atomic_number": 19, "atomic_weight": 39.098, "group": 1, "period": 4, "col": 0, "row": 3},
    {"symbol": "Ca", "name": "Calcium", "atomic_number": 20, "atomic_weight": 40.078, "group": 2, "period": 4, "col": 1, "row": 3},
    # ... add more as needed
]

ELEMENTS_DICT = {e["symbol"]: e for e in ELEMENTS}

# Comprehensive interaction rules: simple and complex
INTERACTIONS = {
    # Simple binary compounds
    frozenset(["Na", "Cl"]): {"product": "NaCl", "desc": "Sodium reacts with Chlorine to form Sodium Chloride (table salt)."},
    frozenset(["K", "Cl"]): {"product": "KCl", "desc": "Potassium reacts with Chlorine to form Potassium Chloride."},
    frozenset(["H", "Cl"]): {"product": "HCl", "desc": "Hydrogen reacts with Chlorine to form Hydrochloric Acid."},
    frozenset(["H", "O"]): {"product": "H2O", "desc": "Hydrogen reacts with Oxygen to form Water."},
    frozenset(["C", "O"]): {"product": "CO2", "desc": "Carbon reacts with Oxygen to form Carbon Dioxide."},
    frozenset(["C", "O2"]): {"product": "CO2", "desc": "Carbon reacts with Oxygen gas to form Carbon Dioxide."},
    frozenset(["C", "O", "O"]): {"product": "CO2", "desc": "Carbon reacts with two Oxygen atoms to form Carbon Dioxide."},
    frozenset(["N", "H"]): {"product": "NH3", "desc": "Nitrogen reacts with Hydrogen to form Ammonia (NH3)."},
    frozenset(["N", "H", "H", "H"]): {"product": "NH3", "desc": "Nitrogen reacts with three Hydrogens to form Ammonia (NH3)."},
    frozenset(["H", "S"]): {"product": "H2S", "desc": "Hydrogen reacts with Sulfur to form Hydrogen Sulfide."},
    frozenset(["Mg", "O"]): {"product": "MgO", "desc": "Magnesium reacts with Oxygen to form Magnesium Oxide."},
    frozenset(["Ca", "O"]): {"product": "CaO", "desc": "Calcium reacts with Oxygen to form Calcium Oxide."},
    frozenset(["Na", "O"]): {"product": "Na2O", "desc": "Sodium reacts with Oxygen to form Sodium Oxide."},
    frozenset(["Fe", "O"]): {"product": "Fe2O3", "desc": "Iron reacts with Oxygen to form Iron(III) Oxide (rust)."},
    frozenset(["Al", "O"]): {"product": "Al2O3", "desc": "Aluminum reacts with Oxygen to form Aluminum Oxide."},
    frozenset(["H", "F"]): {"product": "HF", "desc": "Hydrogen reacts with Fluorine to form Hydrogen Fluoride."},
    frozenset(["H", "Br"]): {"product": "HBr", "desc": "Hydrogen reacts with Bromine to form Hydrogen Bromide."},
    frozenset(["H", "I"]): {"product": "HI", "desc": "Hydrogen reacts with Iodine to form Hydrogen Iodide."},
    frozenset(["Na", "S"]): {"product": "Na2S", "desc": "Sodium reacts with Sulfur to form Sodium Sulfide."},
    frozenset(["K", "O"]): {"product": "K2O", "desc": "Potassium reacts with Oxygen to form Potassium Oxide."},
    frozenset(["Ca", "Cl"]): {"product": "CaCl2", "desc": "Calcium reacts with Chlorine to form Calcium Chloride."},
    frozenset(["Mg", "Cl"]): {"product": "MgCl2", "desc": "Magnesium reacts with Chlorine to form Magnesium Chloride."},
    frozenset(["Al", "Cl"]): {"product": "AlCl3", "desc": "Aluminum reacts with Chlorine to form Aluminum Chloride."},
    frozenset(["Fe", "Cl"]): {"product": "FeCl3", "desc": "Iron reacts with Chlorine to form Iron(III) Chloride."},
    frozenset(["Na", "Br"]): {"product": "NaBr", "desc": "Sodium reacts with Bromine to form Sodium Bromide."},
    frozenset(["K", "Br"]): {"product": "KBr", "desc": "Potassium reacts with Bromine to form Potassium Bromide."},
    frozenset(["Na", "I"]): {"product": "NaI", "desc": "Sodium reacts with Iodine to form Sodium Iodide."},
    frozenset(["K", "I"]): {"product": "KI", "desc": "Potassium reacts with Iodine to form Potassium Iodide."},
    frozenset(["Ca", "Br"]): {"product": "CaBr2", "desc": "Calcium reacts with Bromine to form Calcium Bromide."},
    frozenset(["Ca", "I"]): {"product": "CaI2", "desc": "Calcium reacts with Iodine to form Calcium Iodide."},
    frozenset(["Mg", "Br"]): {"product": "MgBr2", "desc": "Magnesium reacts with Bromine to form Magnesium Bromide."},
    frozenset(["Mg", "I"]): {"product": "MgI2", "desc": "Magnesium reacts with Iodine to form Magnesium Iodide."},
    frozenset(["Al", "Br"]): {"product": "AlBr3", "desc": "Aluminum reacts with Bromine to form Aluminum Bromide."},
    frozenset(["Al", "I"]): {"product": "AlI3", "desc": "Aluminum reacts with Iodine to form Aluminum Iodide."},
    # Complex/Polyatomic and multi-reactant
    frozenset(["Na", "H", "O"]): {"product": "NaOH", "desc": "Sodium reacts with Water to form Sodium Hydroxide."},
    frozenset(["K", "H", "O"]): {"product": "KOH", "desc": "Potassium reacts with Water to form Potassium Hydroxide."},
    frozenset(["Ca", "C", "O"]): {"product": "CaCO3", "desc": "Calcium reacts with Carbon and Oxygen to form Calcium Carbonate (limestone)."},
    frozenset(["Na", "C", "O"]): {"product": "Na2CO3", "desc": "Sodium reacts with Carbon and Oxygen to form Sodium Carbonate."},
    frozenset(["K", "C", "O"]): {"product": "K2CO3", "desc": "Potassium reacts with Carbon and Oxygen to form Potassium Carbonate."},
    frozenset(["Mg", "C", "O"]): {"product": "MgCO3", "desc": "Magnesium reacts with Carbon and Oxygen to form Magnesium Carbonate."},
    frozenset(["H", "C", "O"]): {"product": "H2CO3", "desc": "Hydrogen, Carbon, and Oxygen react to form Carbonic Acid."},
    frozenset(["N", "O"]): {"product": "NO2", "desc": "Nitrogen reacts with Oxygen to form Nitrogen Dioxide."},
    frozenset(["N", "O", "O"]): {"product": "NO2", "desc": "Nitrogen reacts with two Oxygens to form Nitrogen Dioxide."},
    frozenset(["N", "O", "O", "O"]): {"product": "NO3", "desc": "Nitrogen reacts with three Oxygens to form Nitrate ion (NO3-)."},
    frozenset(["S", "O"]): {"product": "SO2", "desc": "Sulfur reacts with Oxygen to form Sulfur Dioxide."},
    frozenset(["S", "O", "O"]): {"product": "SO2", "desc": "Sulfur reacts with two Oxygens to form Sulfur Dioxide."},
    frozenset(["S", "O", "O", "O"]): {"product": "SO3", "desc": "Sulfur reacts with three Oxygens to form Sulfur Trioxide."},
    frozenset(["H", "S", "O"]): {"product": "H2SO4", "desc": "Hydrogen, Sulfur, and Oxygen react to form Sulfuric Acid."},
    frozenset(["H", "N", "O"]): {"product": "HNO3", "desc": "Hydrogen, Nitrogen, and Oxygen react to form Nitric Acid."},
    frozenset(["H", "P", "O"]): {"product": "H3PO4", "desc": "Hydrogen, Phosphorus, and Oxygen react to form Phosphoric Acid."},
    frozenset(["Na", "N", "O"]): {"product": "NaNO3", "desc": "Sodium, Nitrogen, and Oxygen react to form Sodium Nitrate."},
    frozenset(["K", "N", "O"]): {"product": "KNO3", "desc": "Potassium, Nitrogen, and Oxygen react to form Potassium Nitrate."},
    frozenset(["Ca", "N", "O"]): {"product": "Ca(NO3)2", "desc": "Calcium, Nitrogen, and Oxygen react to form Calcium Nitrate."},
    frozenset(["Mg", "N", "O"]): {"product": "Mg(NO3)2", "desc": "Magnesium, Nitrogen, and Oxygen react to form Magnesium Nitrate."},
    # Add more as needed for your application
}

def get_interaction(elements):
    key = frozenset(elements)
    return INTERACTIONS.get(key, None)

def parse_formula(formula):
    """
    Parse a chemical formula into a dict of element symbol -> count.
    Only supports simple formulas (e.g., H2O, CO2, NaCl).
    """
    import re
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    result = {}
    for (sym, count) in tokens:
        if sym not in ELEMENTS_DICT:
            raise ValueError(f"Unknown element: {sym}")
        count = int(count) if count else 1
        result[sym] = result.get(sym, 0) + count
    return result

def formula_weight(formula):
    try:
        parsed = parse_formula(formula)
        return sum(ELEMENTS_DICT[sym]["atomic_weight"] * n for sym, n in parsed.items())
    except Exception:
        return None

class PeriodicTableGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Interactive Periodic Table")
        self.selected_elements = []
        self.selected_buttons = []
        self.create_periodic_table()
        self.create_info_panel()
        self.create_equation_panel()

    def create_periodic_table(self):
        self.table_frame = tk.LabelFrame(self.master, text="Periodic Table")
        self.table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.element_buttons = {}
        for elem in ELEMENTS:
            btn = tk.Button(
                self.table_frame,
                text=elem["symbol"],
                width=4, height=2,
                command=lambda e=elem: self.on_element_click(e)
            )
            btn.grid(row=elem["row"], column=elem["col"], padx=2, pady=2)
            self.element_buttons[elem["symbol"]] = btn

    def create_info_panel(self):
        self.info_frame = tk.LabelFrame(self.master, text="Element Info")
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        self.info_var = tk.StringVar()
        self.info_label = tk.Label(self.info_frame, textvariable=self.info_var, justify="left", font=("Courier", 12))
        self.info_label.pack(padx=5, pady=5)

    def create_equation_panel(self):
        self.eq_frame = tk.LabelFrame(self.master, text="Interaction & Equation")
        self.eq_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.eq_var = tk.StringVar()
        self.eq_label = tk.Label(self.eq_frame, textvariable=self.eq_var, justify="left", font=("Courier", 12), fg="blue")
        self.eq_label.pack(padx=5, pady=5)
        self.clear_btn = tk.Button(self.eq_frame, text="Clear Selection", command=self.clear_selection)
        self.clear_btn.pack(pady=5)

    def on_element_click(self, elem):
        # Deselect if already selected
        if elem["symbol"] in self.selected_elements:
            idx = self.selected_elements.index(elem["symbol"])
            self.selected_elements.pop(idx)
            btn = self.element_buttons[elem["symbol"]]
            btn.config(relief="raised", bg="SystemButtonFace")
            self.selected_buttons.remove(btn)
            self.info_var.set("")
            self.eq_var.set("")
            return

        # Only allow up to 2 elements for interaction demo
        if len(self.selected_elements) >= 2:
            messagebox.showinfo("Selection Limit", "Select up to 2 elements to see their interaction.")
            return

        self.selected_elements.append(elem["symbol"])
        btn = self.element_buttons[elem["symbol"]]
        btn.config(relief="sunken", bg="#b3e6ff")
        self.selected_buttons.append(btn)
        self.show_element_info(elem)

        if len(self.selected_elements) == 2:
            self.show_interaction()

    def show_element_info(self, elem):
        info = (
            f"Symbol: {elem['symbol']}\n"
            f"Name: {elem['name']}\n"
            f"Atomic Number: {elem['atomic_number']}\n"
            f"Atomic Weight: {elem['atomic_weight']}"
        )
        self.info_var.set(info)

    def show_interaction(self):
        interaction = get_interaction(self.selected_elements)
        if interaction:
            product = interaction["product"]
            desc = interaction["desc"]
            reactants = " + ".join(self.selected_elements)
            weight_reactants = sum(ELEMENTS_DICT[sym]["atomic_weight"] for sym in self.selected_elements)
            weight_product = formula_weight(product)
            eqn = f"{reactants} → {product}\n"
            eqn += f"({weight_reactants:.3f} g/mol)   ({weight_product:.3f} g/mol)\n"
            eqn += desc
            self.eq_var.set(eqn)
        else:
            self.eq_var.set("No direct interaction found for selected elements.")

    def clear_selection(self):
        for btn in self.selected_buttons:
            btn.config(relief="raised", bg="SystemButtonFace")
        self.selected_elements.clear()
        self.selected_buttons.clear()
        self.info_var.set("")
        self.eq_var.set("")

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PeriodicTableGUI(root)
    root.mainloop()
