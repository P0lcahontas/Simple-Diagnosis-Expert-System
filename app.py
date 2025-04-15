from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'history.json'

class KnowledgeBase:
    def __init__(self):
        self.diseases = {
            "Common Cold": {"symptoms": ["sneezing", "runny_nose"], "treatment": "rest and fluids", "severity": 1},
            "Flu": {"symptoms": ["fever", "cough", "body_aches"], "treatment": "rest and fluids", "severity": 2},
            "Pneumonia": {"symptoms": ["fever", "cough", "shortness_of_breath"], "treatment": "antibiotics", "severity": 3},
            "Tuberculosis": {"symptoms": ["cough", "weight_loss", "night_sweats"], "treatment": "antibiotics", "severity": 4},
            "Bronchitis": {"symptoms": ["cough", "chest_pain", "fatigue"], "treatment": "rest and fluids", "severity": 2},
            "COVID-19": {"symptoms": ["fever", "cough", "shortness_of_breath", "loss_of_taste", "fatigue"], "treatment": "isolation and rest", "severity": 3},
            "Asthma": {"symptoms": ["shortness_of_breath", "wheezing", "chest_tightness", "coughing_at_night"], "treatment": "inhalers and avoidance of triggers", "severity": 2},
            "Allergy": {"symptoms": ["sneezing", "runny_nose", "itchy_eyes", "skin_rash"], "treatment": "antihistamines", "severity": 1},
            "Sinusitis": {"symptoms": ["headache", "nasal_congestion", "facial_pain", "runny_nose"], "treatment": "decongestants", "severity": 2},
            "Lung Cancer": {"symptoms": ["persistent_cough", "chest_pain", "weight_loss", "coughing_blood"], "treatment": "chemotherapy", "severity": 4},
            "COVID Long Haul": {"symptoms": ["fatigue", "brain_fog", "joint_pain", "shortness_of_breath"], "treatment": "supportive care", "severity": 3},
            "Migraine": {"symptoms": ["headache", "nausea", "sensitivity_to_light", "sensitivity_to_sound"], "treatment": "pain relievers", "severity": 2},
            "Malaria": {"symptoms": ["fever", "chills", "sweating", "nausea", "vomiting"], "treatment": "antimalarial drugs", "severity": 4},
            "Dengue": {"symptoms": ["fever", "rash", "muscle_pain", "bleeding_gums"], "treatment": "fluid replacement", "severity": 4}
        }
        

        self.relationships = {}
        for disease, data in self.diseases.items():
            for symptom in data["symptoms"]:
                self.relationships.setdefault(symptom, []).append(disease)

    def get_disease(self, symptoms):
        possible = {}
        for symptom in symptoms:
            for disease in self.relationships.get(symptom, []):
                possible[disease] = possible.get(disease, 0) + 1

        matches = []
        for disease, count in possible.items():
            required_symptoms = self.diseases[disease]["symptoms"]
            probability = count / len(required_symptoms)
            severity = self.diseases[disease]["severity"]
            if probability > 0.5:
                matches.append((disease, probability, severity))

        return sorted(matches, key=lambda x: (-x[1], -x[2]))

def load_history():
    if os.path.exists(DATA_FILE):
        if os.path.getsize(DATA_FILE) == 0:  # check if the file is empty
            return []
        with open(DATA_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # fallback if file has bad JSON
    return []


def save_history(history):
    with open(DATA_FILE, 'w') as file:
        json.dump(history, file, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    kb = KnowledgeBase()
    relationships = list(kb.relationships.keys())
    diagnoses = []

    if request.method == 'POST':
        input_symptoms = request.form.get('symptoms', '')
        symptoms = [s.strip().lower().replace(" ", "_") for s in input_symptoms.split(',') if s.strip()]
        diagnoses = kb.get_disease(symptoms)

        if diagnoses:
            history = load_history()
            for disease, prob, _ in diagnoses:
                history.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "symptoms": symptoms,
                    "diagnosis": disease,
                    "probability": round(prob, 2)
                })
            save_history(history)

    return render_template('index.html', relationships=relationships, diagnoses=diagnoses)

@app.route('/history')
def history():
    history = load_history()
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
