from unstructured.partition.auto import partition,  # Base Function to Partition PDF
from unstructured.staging.base import (
    convert_to_dict,
)  # Convert List Unstructured Elements Into List of Dicts for Easy Parsing
from unstructured.cleaners.core import (
    clean,
    remove_punctuation,
    clean_non_ascii_chars,
)  # Cleaning Functions
import re  # Create Custom Cleaning Function
import nltk  # Toolkit for more advanced pre-processing
from nltk.corpus import stopwords  # list of stopwords to remove
from typing import List  # Type Hinting


# Returns a List[Element] present in the pages of the parsed pdf document
elements = partition("../data/ev_outlook_2023.pdf")

for e in elements:
    print(e)

