import joblib
import matplotlib.pyplot as plt
import pandas as pd

model = joblib.load("models/ids_model.pkl")

features = [
    'logged_in','serror_rate','srv_serror_rate','same_srv_rate',
    'dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate','dst_host_serror_rate','dst_host_srv_serror_rate'
]

importance = pd.Series(model.feature_importances_, index=features).sort_values()

importance.plot(kind='barh', figsize=(8,5), color='steelblue')
plt.title('Feature Importance')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('models/feature_importance.png')
print("Feature importance chart saved to models/feature_importance.png")