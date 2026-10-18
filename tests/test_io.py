import pytest
from tqdm import tqdm
from bikenetlib import constants, io

from bikenetlib.io import (
    slugify,
    initialize_progress_bar,
)

# slugify
@pytest.fixture
def city_names():
    names = ["Aix-En-Provence", "Alcalá De Henares", "Almería", "Bielsko-Biala", "Chișinău", "Durrës", "L'Hospitalet De Llobregat", "Nîmes", "Umeå", "amsterdam_nl", "áéíóúàèìùòâêîôûäëïöüǎěǐǒǔãẽĩõũăåæçčıłñňøœřßșşšůŷÿźž"]
    return names

@pytest.fixture
def city_names_slugified():
    names = ["aixenprovence", "alcaladehenares", "almeria", "bielskobiala", "chisinau", "durres", "lhospitaletdellobregat", "nimes", "umea", "amsterdam_nl", "aeiouaeiouaeiouaeiouaeiouaeiouaaaccilnnoorssssuyyzz"]
    return names

def test_slugify(city_names, city_names_slugified):
    for n, ns in zip(city_names, city_names_slugified):
        assert slugify(n) == ns


@pytest.fixture
def progress_bar_string():
    return "Test string"

def test_initialize_progress_bar(progress_bar_string):
    tqdm_left = initialize_progress_bar(progress_bar_string, total=1, unit="step")
    tqdm_right = tqdm(
        desc=("{:<"+str(constants._PROGRESS_BAR_DESC_LENGTH)+"}").format(progress_bar_string),
        total=1,
        unit="step",
        bar_format='{l_bar}{bar:'+str(constants._PROGRESS_BAR_LENGTH-7)+'}{r_bar}',
        disable=io.silent,
    )
    assert tqdm_left.desc == tqdm_right.desc
