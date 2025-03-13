import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")  # 샘플 데이터
sns.scatterplot(x="total_bill", y="tip", data=tips, hue="sex")

plt.title("Seaborn Scatter Plot")
plt.show()