from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# load and preprocess data
data = pd.read_csv('data.csv')
features_selected = [
    'radius_mean', 'texture_mean', 'smoothness_mean', 'compactness_mean',
    'concavity_mean', 'symmetry_mean', 'radius_se', 'concave points_se',
    'smoothness_worst', 'compactness_worst', 'concavity_worst',
    'symmetry_worst', 'fractal_dimension_worst'
]
X = data[features_selected].dropna()
y = data['diagnosis'].dropna()
X = X.loc[y.index]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=23)

# train RF
best_rf = RandomForestClassifier(
    bootstrap=False,
    max_depth=10,
    max_features='sqrt',
    min_samples_leaf=1,
    min_samples_split=5,
    n_estimators=100,
    random_state=23
)
best_rf.fit(X_train, y_train)

@app.route('/')
def index():
    # render frontend
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
# main function for classification based on input 
def predict():
    try:
        input = request.json
        
        missing = [f for f in features_selected if f not in input]
        if missing:
            raise ValueError(f"Missing features: {', '.join(missing)}")
        
        input_df = pd.DataFrame([input])
        
        prediction = best_rf.predict(input_df)[0]
        pred_prob = best_rf.predict_proba(input_df).tolist()[0]
        
        pred_label = "Benign" if prediction == "B" else "Malignant"
        
        return jsonify({
            "prediction": pred_label,
            "probabilities": {
                "Benign": pred_prob[0],
                "Malignant": pred_prob[1]
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
