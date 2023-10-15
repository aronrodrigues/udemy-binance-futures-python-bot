import pandas as pd

record = {
    "name": ["Aron", "Bernardo", "Carol"],
    "age": [41, 5, 40],
    "gender": ["m", "m", "f"],
}

df = pd.DataFrame(record)
print("\n--- DataFrame")
print(df)


print("\n--- Series")
print(df["name"])

print("\n---\n Dataframe + Column")
print(df[["name"]])

print("\n--- Specific Row")
print(df.loc[1])

print("\n--- Sub DataFrame")
print(df.loc[[1, 2]])

print("\n--- Condition")
print(df.loc[df.age > 40])

print("\n--- Condition + Column")
print(df.loc[df.age < 10]["name"])

print("\n--- Iteration")
for i in df.index:
    print(df.gender[i])
