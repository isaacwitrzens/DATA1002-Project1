import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#loading the file
combined_file = r"C:\Users\witrz\PycharmProjects\DATA1002\Data Files - Clean\Combined_Crime_Liquor_Hosp.csv"
df = pd.read_csv(combined_file)

#making scatter plot with numpy to introduce trendline
x = df["TotalCrimes"]
y = df["license_count"]
m, b = np.polyfit(x, y, 1)
plt.scatter(x, y, s=10)
plt.plot(x, m*x + b, color="red")
plt.xlabel("Total Crimes")
plt.ylabel("Liquor License Count")
plt.title("Liquor License Count vs Total Crimes")

#equation, r and r squared calcs
y_pred = m*x + b
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - (ss_res / ss_tot)
eq_text = f"y = {m:.4f}x + {b:.2f}\nR² = {r2:.3f}"
plt.text(0.05, 0.88, eq_text, transform=plt.gca().transAxes,
         fontsize=10, verticalalignment="top", color="red")

r = x.corr(y)
plt.text(0.05, 0.80, f"r = {r:.3f}", transform=plt.gca().transAxes,
         fontsize=10, verticalalignment="top", color="blue")

plt.show()

