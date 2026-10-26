"""Import/Output functions of `bikenetlib`, including format conversions and 
user feedback tools.

silent : bool, default False
    If set to True, suppresses all user feedback. Useful for batch exports.
"""

silent = False

import re
from tqdm import tqdm
from . import constants, osm, _overpass

def slugify(s): 
    """Slugify a string.
    
    Adapted from: https://github.com/Chalarangelo/30-seconds-of-code/blob/master/content/snippets/python/s/slugify.md

    Parameters
    ----------
    s : str
        String to slufigy.

    Returns
    -------
    s : str
        Slugified string.

    Notes
    -----
    A clean global solution would be using unidecode, but we do not want
    extra dependencies for this. We assume European city names in latin
    alphabet, and some special letters like Hungarian ő already mapped.
    """
    s = s.lower().strip()
    s = re.sub(r'[\s-]+', '', s) # Remove white spaces, -
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'^-+|-+$', '', s)
    tab = str.maketrans(
        "áéíóúàèìùòâêîôûäëïöüǎěǐǒǔãẽĩõũăåæçčıłñňøœřßșşšůŷÿźž",
        "aeiouaeiouaeiouaeiouaeiouaeiouaaaccilnnoorssssuyyzz"
    )
    s = s.translate(tab)
    return s


def initialize_progress_bar(desc_string, total=1, unit="step"):
    """Initialize tqdm progress bar.
    """
    return tqdm(
        desc=("{:<"+str(constants._PROGRESS_BAR_DESC_LENGTH)+"}").format(desc_string),
        total=total,
        unit=unit,
        bar_format='{l_bar}{bar:'+str(constants._PROGRESS_BAR_LENGTH-7)+'}{r_bar}',
        disable=silent,
    )
