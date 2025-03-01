# %%
import os
from collections import defaultdict
from datetime import date

import pandas as pd

# %%

input_dir = "../../data/in_process"
output_dir = "../../data/questions"

# %%
# read all the files in the input directory

files = os.listdir(input_dir)
print(len(files))

# %%
# identify the questions in each file

questions = {}
for file in files:
    # print the filename and the number of labels
    print(file)
    # First try reading without specifying dtype for amount to see which rows fail conversion (if any)
    try:
        df = pd.read_csv(os.path.join(input_dir, file))
        # Now attempt to convert amount column to float to find problematic row
        pd.to_numeric(df["amount"], errors="raise")
    except ValueError as e:
        print(f"Error converting amount to float in file {file}:")
        print(e)
        # Get the problematic rows
        mask = pd.to_numeric(df["amount"], errors="coerce").isna()
        print("\nProblematic rows:")
        print(df[mask])

    # Now read with proper dtypes
    df = pd.read_csv(
        os.path.join(input_dir, file),
        dtype={"user_id": str, "name": str, "date": str, "amount": float, "recurring": str},
    )
    # create a dictionary whose key is "user_id/name" and whose value is a list of (amount, recurring) tuples
    labels = defaultdict(list)
    for index, row in df.iterrows():
        user_id = row["user_id"]
        name = row["name"]
        _date = row["date"]
        amount = row["amount"]
        recurring = row["recurring"].strip() if pd.notna(row["recurring"]) else ""
        labels[f"{user_id}/{name}"].append((_date, amount, recurring))
    # keep only the labels where at least one of the recurring values is a '?'
    labels = {k: v for k, v in labels.items() if any(recurring == "?" for _, _, recurring in v)}
    # add the labels to the questions dictionary
    questions.update(labels)
    # print the filename and the number of labels
    print(len(labels))
# print the number of keys in the questions dictionary and the total number of labels
print(len(questions))
print(sum(len(v) for v in questions.values()))

# %%
# save the questions to a dataframe where the (date, amount, recurring) tuples are in separate columns,
# and save the dataframe to a csv file

# only save each name once
seen_names = set()
# Create list of rows with user_id, name, date, amount, recurring
rows = []
for key, tuples in questions.items():
    user_id, name = key.split("/", maxsplit=1)
    if name in seen_names:
        continue
    seen_names.add(name)
    for _date, amount, recurring in tuples:
        rows.append({"user_id": user_id, "name": name, "date": _date, "amount": amount, "recurring": recurring})
df = pd.DataFrame(rows)
today = date.today().strftime("%Y-%m-%d")
df.to_csv(os.path.join(output_dir, f"{today}.csv"), index=False)


# %%
