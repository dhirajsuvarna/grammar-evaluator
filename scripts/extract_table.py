import pandas as pd
import docx  # from python-docx package
import re


def remove_html_tags(iText):
    return re.sub("<[^<]+?>", "", iText)


# Load the Word Document

# doc_path = r"../data/studmodassess-07-02-24.docx"
doc_path = r"../data/studtopicassess-08-02-2024.docx"
doc = docx.Document(doc_path)

# Assuming you want to extract the first table
table = doc.tables[0]

# Create an empty list to hold the row data
data = []

# Iterate over the table rows and cells
for row in table.rows:
    row_data = []
    for cell in row.cells:
        row_data.append(cell.text)
    data.append(row_data)

# Convert the data into a pandas DataFrame
# First row in data is assumed to be the column headers
df = pd.DataFrame(data[1:], columns=data[0])
print(df.shape)
print(df)
df["CLEANED_ANSWER"] = df["GRAMMAR_CHECKED_ANSWER"].apply(remove_html_tags)

print(df.shape)
print(df)

# outpath = r"../data/studmodassess-07-02-24.csv"
outpath = r"../data/studtopicassess-08-02-2024.csv"
df.to_csv(outpath, encoding="utf-8", index=False)
