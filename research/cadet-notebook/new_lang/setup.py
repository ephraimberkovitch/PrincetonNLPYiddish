
from setuptools import setup
setup(
    name="yi",
    entry_points={
        "spacy_languages": ["yi = yi:Yiddish"],
    }
)
