import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("StudentsPerformance.csv")

train, temp = train_test_split(df, test_size=0.3, random_state=42)
eval_df, serving = train_test_split(temp, test_size=0.5, random_state=42)

train.to_csv("data/train/data.csv", index=False)
eval_df.to_csv("data/eval/data.csv", index=False)
serving.to_csv("data/serving/data.csv", index=False)

print("Done! Files saved.")
