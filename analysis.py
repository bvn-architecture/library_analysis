#%%
import os
import json

import pandas as pd
from tinydb import Query, TinyDB

#%% set up the DB
db = TinyDB("library.json", sort_keys=True, indent=4)
q = Query()

#%% Load the library CSV
book_table_df = pd.read_excel("Library Books.xlsx")
# book_table_df = book_table_df.head(20)
book_table_df.head()

# %% This section makes a DB of the books and authors:
# There are a lot of things still to do with this, i.e. there's no studio split etc.
book_table = db.table("books")
author_table = db.table("authors")

#%% Make a little viz of the subjects in the library

subjects = []
for s in book_table_df.Subject:
    if type(s) is str:
        subjects.extend(s.split("|"))
print(f"there are {len(set(subjects))} unique subjects")
svc = pd.Series(subjects).value_counts()
svc[svc > 10].plot(kind="barh", figsize=(6, 10))
#%%
def get_role(a):
    role = ""
    if "(ed)" in a:
        role = "editor"
    return role


def insert_authors(authors_str, book_title):
    ids = []
    if type(authors_str) is str:
        a_list = authors_str.split("|")
        for a in a_list:
            # role = get_role(a) #TODO: role is on a per book basis, so that relationship needs to be a bit more complicated
            author_name = a.replace("(ed)", "").strip()
            id = author_table.upsert(
                {"author_name": author_name},
                q.author_name == author_name,
            )
            ids.append(id[0])
    return ids


# %%
for i, row in book_table_df.iterrows():
    book_title = row.Title
    authors_str = row.Author
    subject = row.Subject
    author_ids = insert_authors(authors_str, book_title)
    book_id = book_table.upsert(
        {"book_title": book_title, "authors": author_ids},
        q.book_title == book_title,
    )


# %% So now we have a DB, we can load it back in as dataframes and do some things to it
# Not the most efficient way to do this, I'm sure, but we do also get a DB while we're at it
with open("library.json", "r", encoding="utf-8") as lib_json:
    library_json = json.load(lib_json)

#%%
bj = []
for k, d in library_json["books"].items():
    print(k, d)
    d["id"] = k
    bj.append(d)

book_df = pd.DataFrame(bj)
book_df.set_index("id", inplace=True)
book_df.head()

#%%
aj = []
for k, d in library_json["authors"].items():
    print(k, d)
    d["id"] = k
    aj.append(d)

author_df = pd.DataFrame(aj)
author_df.set_index("id", inplace=True)
author_df["book_list"] = author_df.apply(lambda _: [], axis=1)
author_df.head()

#%% Make a backreference to the books so we can tell who wrote what.
for i, row in book_df.iterrows():
    if len(row.authors) != 0:
        for a_id in row.authors:
            old_bl = author_df.loc[str(a_id)].book_list
            if type(old_bl) is tuple:
                old_bl = old_bl[0]
            new_bl = list(set(old_bl + [row.book_title]))
            author_df.loc[str(a_id)].book_list = new_bl

author_df["book_count"] = author_df["book_list"].apply(lambda x: len(x))

author_df.head()
# %% dump to a csv to start adding extra columns
author_df.to_csv("authors.csv")

# %%
