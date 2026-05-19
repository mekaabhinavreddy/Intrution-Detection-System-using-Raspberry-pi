import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
import joblib

cols = [
    'duration','protocol_type','service','flag',
    'src_bytes','dst_bytes','land','wrong_fragment',
    'urgent','hot','num_failed_logins','logged_in',
    'num_compromised','root_shell','su_attempted',
    'num_root','num_file_creations','num_shells',
    'num_access_files','num_outbound_cmds',
    'is_host_login','is_guest_login','count',
    'srv_count','serror_rate','srv_serror_rate',
    'rerror_rate','srv_rerror_rate','same_srv_rate',
    'diff_srv_rate','srv_diff_host_rate',
    'dst_host_count','dst_host_srv_count',
    'dst_host_same_srv_rate','dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate','dst_host_srv_serror_rate',
    'dst_host_rerror_rate','dst_host_srv_rerror_rate',
    'label','difficulty'
]

df = pd.read_csv('data/KDDTrain+.txt', names=cols)

attack_map = {
    'normal':'normal',
    'neptune':'dos','smurf':'dos','pod':'dos',
    'teardrop':'dos','land':'dos','back':'dos',
    'ipsweep':'probe','portsweep':'probe',
    'nmap':'probe','satan':'probe',
    'ftp_write':'r2l','guess_passwd':'r2l',
    'imap':'r2l','multihop':'r2l','phf':'r2l',
    'spy':'r2l','warezclient':'r2l','warezmaster':'r2l',
    'buffer_overflow':'u2r','loadmodule':'u2r',
    'perl':'u2r','rootkit':'u2r'
}
df['label'] = df['label'].map(attack_map).fillna('other')

le = LabelEncoder()
for col in ['protocol_type','service','flag']:
    df[col] = le.fit_transform(df[col])

X = df.drop(['label','difficulty'], axis=1)
y = df['label']

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

selector = SelectKBest(chi2, k=10)
X_selected = selector.fit_transform(X_scaled, y)

selected_features = X.columns[selector.get_support()].tolist()
print('Top 10 features:', selected_features)

X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.2, random_state=42, stratify=y
)

joblib.dump(scaler,    'models/scaler.pkl')
joblib.dump(selector,  'models/selector.pkl')
joblib.dump((X_train, X_test, y_train, y_test), 'models/data_split.pkl')

print('Preprocessing done.')
print(f'Train: {X_train.shape}, Test: {X_test.shape}')