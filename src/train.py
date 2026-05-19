from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

X_train, X_test, y_train, y_test = joblib.load("models/data_split.pkl")

model = DecisionTreeClassifier(max_depth=15, min_samples_split=5, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", round(accuracy_score(y_test, y_pred)*100, 2), "%")
print()
print(classification_report(y_test, y_pred))

joblib.dump(model, "models/ids_model.pkl")
print("Model saved to models/ids_model.pkl")

cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=model.classes_, yticklabels=model.classes_)
plt.title("Confusion Matrix")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("models/confusion_matrix.png")
print("Confusion matrix saved to models/confusion_matrix.png")