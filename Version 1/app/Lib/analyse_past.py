import pandas as pd 


file = "OnePiceV02_Histo.csv"
data = pd.read_csv(file)

# Affichage Columns Du Fichier
# print(data.columns)


# Recuperation des Donner Utile a notre Analyse
Nb_Position_symbol = data.value_counts(['symbol',"type","comment","profit","fee"])

Nb_Position_symbol.to_csv("Pre-Analyse_Challenge1.csv")
print(Nb_Position_symbol)