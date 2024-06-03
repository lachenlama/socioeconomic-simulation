import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Generate synthetic data
np.random.seed(42)
num_samples = 1000
data = {
    "gdp_growth": np.random.uniform(-0.05, 0.05, num_samples),
    "inflation_rate": np.random.uniform(0, 0.1, num_samples),
    "unemployment_rate": np.random.uniform(0, 0.2, num_samples),
    "income": np.random.uniform(30000, 100000, num_samples),
    "savings": np.random.uniform(0, 50000, num_samples),
    "debt": np.random.uniform(0, 20000, num_samples),
    "happiness": np.random.randint(0, 101, num_samples)
}

df = pd.DataFrame(data)

# Ensure all happiness values are within the range 0 to 100
df["happiness"] = df["happiness"].clip(0, 100)

# Define features and target
features = ["gdp_growth", "inflation_rate", "unemployment_rate", "income", "savings", "debt"]
target = "happiness"

# Convert happiness into categories: 0 (unhappy), 1 (neutral), 2 (happy)
bins = [0, 30, 70, 100]
labels = [0, 1, 2]
df["happiness"] = pd.cut(df["happiness"], bins=bins, labels=labels)

# Drop any rows with NaN values in the target column
df.dropna(subset=["happiness"], inplace=True)

X = df[features]
y = df["happiness"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a decision tree classifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

# Save the model using joblib
joblib.dump(model, "happiness_model.pkl")
