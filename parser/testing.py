import pandas as pd
import os

file_names = os.listdir("C:\\Users\This Pc\PycharmProjects\\askdata\data-xsl")

name = file_names[1]
name = "C:\\Users\This Pc\PycharmProjects\\askdata\data-xsl\\" + name
df = pd.read_excel(name)
len_col = len(df.index)
for w in df.columns:
    print(w)