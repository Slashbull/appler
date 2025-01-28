from sklearn.ensemble import IsolationForest

def detect_anomalies(data):
    """
    Use Isolation Forest to detect anomalies in import trends.
    """
    model = IsolationForest(contamination=0.05, random_state=42)
    data['Anomaly'] = model.fit_predict(data[['Quantity']])
    anomalies = data[data['Anomaly'] == -1]
    return anomalies
