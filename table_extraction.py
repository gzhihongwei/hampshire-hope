import tabula
import numpy as np
import pandas as pd


dfs = tabula.read_pdf("city_town.pdf", pages='all')

tabula.convert_into("city_town.pdf", "output.csv", output_format="csv", pages='all')

residence_of_decedent = pd.concat(dfs[:10])
town_of_death_occurrence = pd.concat(dfs[10:])

residence_of_decedent.to_csv("residence_of_decedent.csv")
town_of_death_occurrence.to_csv("town_of_death_occurence.csv")