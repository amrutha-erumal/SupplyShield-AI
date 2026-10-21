
import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# Reproducible synthetic training data
rng = np.random.default_rng(42)
n = 2000

data = pd.DataFrame({
    "lead_time_days": rng.integers(2, 31, n),
    "supplier_delay_rate": rng.uniform(0, 0.8, n),
    "order_volume": rng.integers(10, 1001, n),
    "inventory_days": rng.integers(0, 31, n),
    "weather_risk": rng.uniform(0, 1, n),
    "transport_risk": rng.uniform(0, 1, n),
})

# Simulated probability of a late delivery.
# These rules are assumptions for a demo, not real supplier data.
risk_score = (
    -2.0
    + 0.045 * data["lead_time_days"]
    + 3.0 * data["supplier_delay_rate"]
    - 0.055 * data["inventory_days"]
    + 1.2 * data["weather_risk"]
    + 1.5 * data["transport_risk"]
    + 0.0003 * data["order_volume"]
)

probability = 1 / (1 + np.exp(-risk_score))
data["delayed"] = rng.binomial(1, probability)

features = [
    "lead_time_days",
    "supplier_delay_rate",
    "order_volume",
    "inventory_days",
    "weather_risk",
    "transport_risk",
]

X = data[features]
y = data["delayed"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=5,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\n=== SUPPLYSHIELD AI MODEL REPORT ===")
print(f"Training records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")
print(f"Test accuracy: {accuracy_score(y_test, predictions):.2%}")
print(f"ROC-AUC: {roc_auc_score(y_test, probabilities):.3f}")
print("\nClassification report:")
print(classification_report(y_test, predictions))
print("Confusion matrix:")
print(confusion_matrix(y_test, predictions))

os.makedirs("models", exist_ok=True)

joblib.dump(
    {"model": model, "features": features},
    "models/supplier_risk_model.joblib"
)

print("\nModel saved to models/supplier_risk_model.joblib")
print("Note: Results reflect synthetic data, not real supplier performance.")
