from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
import numpy as np

data_file = "data.csv"
fields = []
rows = []

with open(data_file, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
    # extracting field names through first row
    fields = next(csvreader)
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
doc = []
for row in rows:
  doc.append(row[2])
vectorizer = TfidfVectorizer()
docs_TfIdf = vectorizer.fit_transform(doc)
#list(vectorizer.vocabulary_.keys())
query = "PHP Variables"
tf_idf_query = vectorizer.transform([query])

cosine = []
for d in tqdm(docs_TfIdf):
  cosine.append(float(cosine_similarity(d,tf_idf_query)))
sorted_id = np.argsort(cosine)
for i in range(10):
  curr_id = sorted_id[-i-1]
  print(doc[curr_id],cosine[curr_id])
  print("*"*100)