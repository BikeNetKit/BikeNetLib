import pytest

from bikenetlib.io import (
    slugify,
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