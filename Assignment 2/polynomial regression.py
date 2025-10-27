# --- polynomial_regression_tuned.py ---
# Tune polynomial degree on validation set, refit on train+valid,
# report final metrics on test, then produce tuning and final-result plots.

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -------------------------------
# File paths (update if needed)
# -------------------------------
BASE = r"C:\Users\witrz\PycharmProjects\DATA1002\Assignment 2"
TRAIN = os.path.join(BASE, "train.csv")
VALID = os.path.join(BASE, "valid.csv")
TEST  = os.path.join(BASE, "test.csv")
VAL_SUMMARY_OUT = os.path.join(BASE, "poly_valid_summary.csv")
TEST_PRED_OUT   = os.path.join(BASE, "poly_test_predictions.csv")
PLOT_DIR        = os.path.join(BASE, "isaac plots")

# -------------------------------
# Load data
# -------------------------------
train = pd.read_csv(TRAIN)
valid = pd.read_csv(VALID)
test  = pd.read_csv(TEST)

# -------------------------------
# Select features (X) and target (y)
# - Drop ID-like columns (e.g., Suburb)
# - Keep numeric licence columns; target is TotalCrimes
# -------------------------------
FEATURE_EXCLUDE = {"TotalCrimes", "Suburb"}

X_train = train[[c for c in train.columns if c not in FEATURE_EXCLUDE]].copy()
y_train = train["TotalCrimes"].copy()

X_valid = valid[[c for c in valid.columns if c not in FEATURE_EXCLUDE]].copy()
y_valid = valid["TotalCrimes"].copy()

X_test  = test[[c for c in test.columns if c not in FEATURE_EXCLUDE]].copy()
y_test  = test["TotalCrimes"].copy()

print("Features used:", list(X_train.columns))

# -------------------------------
# Helper to build a model pipeline for a chosen degree
# Pipeline: PolynomialFeatures -> StandardScaler -> LinearRegression
# -------------------------------
def make_poly_model(degree: int) -> Pipeline:
    return Pipeline([
        ("poly",   PolynomialFeatures(degree=degree, include_bias=False)),
        ("scale",  StandardScaler()),
        ("linreg", LinearRegression())
    ])

# -------------------------------
# Helper to compute metrics
# (RMSE = sqrt(MSE) for compatibility with all sklearn versions)
# -------------------------------
def eval_reg(y_true, y_pred):
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    r2   = r2_score(y_true, y_pred)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}

# -------------------------------
# Tune degree on the validation set
# -------------------------------
DEGREES_TO_TRY = [1, 2, 3]  # 1=linear baseline; 2..4 allow curvature
val_rows = []

for d in DEGREES_TO_TRY:
    model = make_poly_model(d)
    model.fit(X_train, y_train)             # fit on training only
    yv = model.predict(X_valid)             # predict on validation
    metrics = eval_reg(y_valid, yv)
    metrics["Degree"] = d
    val_rows.append(metrics)
    print(f"[degree={d}] VALID -> R2={metrics['R2']:.3f}, RMSE={metrics['RMSE']:.3f}, MAE={metrics['MAE']:.3f}")

# Build validation summary and choose best degree by lowest RMSE
val_df = pd.DataFrame(val_rows).sort_values("RMSE").reset_index(drop=True)
best_degree = int(val_df.iloc[0]["Degree"])
print("\nValidation ranking (by RMSE):")
print(val_df.to_string(index=False))
print(f"\n✅ Best polynomial degree by validation RMSE = {best_degree}")

# Save validation summary
val_df.to_csv(VAL_SUMMARY_OUT, index=False)

# -------------------------------
# Refit best-degree model on TRAIN + VALID
# -------------------------------
X_final = pd.concat([X_train, X_valid], axis=0).reset_index(drop=True)
y_final = pd.concat([y_train, y_valid], axis=0).reset_index(drop=True)

final_model = make_poly_model(best_degree)
final_model.fit(X_final, y_final)

# -------------------------------
# Final evaluation on TEST (report these)
# -------------------------------
yt_pred = final_model.predict(X_test)
test_metrics = eval_reg(y_test, yt_pred)
print(f"\n📊 TEST (degree={best_degree}) -> "
      f"R2={test_metrics['R2']:.3f}, RMSE={test_metrics['RMSE']:.3f}, MAE={test_metrics['MAE']:.3f}")

# Save test predictions for plots
pd.DataFrame({"y_test": y_test.values, "y_pred": yt_pred}).to_csv(TEST_PRED_OUT, index=False)
print(f"Saved:\n- Validation summary -> {VAL_SUMMARY_OUT}\n- Test predictions -> {TEST_PRED_OUT}")

# -------------------------------
# PLOTTING: tuning curves + final diagnostics
# -------------------------------
os.makedirs(PLOT_DIR, exist_ok=True)

sns.set(style="whitegrid", font_scale=1.2)

val_df_plot = val_df.sort_values("Degree")

# ---------------------------
# RMSE vs Degree
# ---------------------------
plt.figure(figsize=(7,5))
sns.lineplot(
    data=val_df_plot, x="Degree", y="RMSE",
    marker="o", linewidth=2.5, color="#2E86AB"
)
best_row = val_df_plot.loc[val_df_plot["RMSE"].idxmin()]
plt.scatter(best_row["Degree"], best_row["RMSE"], color="#E74C3C", s=100, zorder=5)
plt.annotate(
    f"Best = {int(best_row['Degree'])}\nRMSE = {best_row['RMSE']:.2f}",
    (best_row["Degree"], best_row["RMSE"]),
    xytext=(10, 30), textcoords="offset points",
    arrowprops=dict(arrowstyle="->", color="#E74C3C")
)
plt.title("Polynomial Degree vs RMSE", fontsize=14, weight="bold")
plt.xlabel("Polynomial Degree")
plt.ylabel("RMSE")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "poly_valid_rmse.png"), dpi=300)
plt.close()

# ---------------------------
# R² vs Degree
# ---------------------------
plt.figure(figsize=(7,5))
sns.lineplot(
    data=val_df_plot, x="Degree", y="R2",
    marker="o", linewidth=2.5, color="#1ABC9C"
)
best_row_r2 = val_df_plot.loc[val_df_plot["R2"].idxmax()]
plt.scatter(best_row_r2["Degree"], best_row_r2["R2"], color="#E67E22", s=100, zorder=5)
plt.annotate(
    f"Best = {int(best_row_r2['Degree'])}\nR² = {best_row_r2['R2']:.2f}",
    (best_row_r2["Degree"], best_row_r2["R2"]),
    xytext=(10, -30), textcoords="offset points",
    arrowprops=dict(arrowstyle="->", color="#E67E22")
)
plt.title("Polynomial Degree vs R² (Validation)", fontsize=14, weight="bold")
plt.xlabel("Polynomial Degree")
plt.ylabel("R²")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "poly_valid_r2.png"), dpi=300)
plt.close()

# 2) Predicted vs Actual (test) + Residuals
from sklearn.metrics import mean_squared_error as _mse, mean_absolute_error as _mae, r2_score as _r2
# (already imported; kept here to show intent)

y_test_arr = y_test.values
y_pred_arr = yt_pred

# Pred vs Actual
plt.figure()
plt.scatter(y_test_arr, y_pred_arr, s=16)
lims = [min(y_test_arr.min(), y_pred_arr.min()), max(y_test_arr.max(), y_pred_arr.max())]
plt.plot(lims, lims)
plt.title(f"Predicted vs Actual\nR²={test_metrics['R2']:.3f}, RMSE={test_metrics['RMSE']:.2f}, MAE={test_metrics['MAE']:.2f}")
plt.xlabel("Actual TotalCrimes")
plt.ylabel("Predicted TotalCrimes")
plt.savefig(os.path.join(PLOT_DIR, "poly_test_pred_vs_actual.png"), dpi=200)
plt.close()

# Residuals
residuals = y_test_arr - y_pred_arr
plt.figure()
plt.hist(residuals, bins=20)
plt.title("Residuals — Polynomial Regression")
plt.xlabel("Error = Actual - Predicted")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, "poly_test_residuals_hist.png"), dpi=200)
plt.close()


print("Saved plots to:", PLOT_DIR)