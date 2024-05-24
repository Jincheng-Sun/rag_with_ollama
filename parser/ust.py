from unstructured.partition.auto import partition

# Returns a List[Element] present in the pages of the parsed pdf document
elements = partition("../data/ev_outlook_2023.pdf")

for e in elements:
    print(e)
