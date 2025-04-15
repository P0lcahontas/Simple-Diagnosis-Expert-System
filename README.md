# Simple-Diagnosis-Expert-System

🩺 Medical Diagnosis System
This is a simple web-based medical diagnosis system built with Flask. It allows users to input symptoms and receive possible disease diagnoses based on a knowledge base of common illnesses.

⚙️ Features
Diagnose possible diseases based on entered symptoms

Shows probability and severity of each diagnosis

View past diagnosis history

Simple and extensible knowledge base

📂 Project Structure
bash
Copy
Edit
/project-root
│
├── app.py                 # Main Flask app
├── history.json           # Stores diagnosis history
├── templates/
│   ├── index.html         # Main page
│   └── history.html       # History page
├── static/
│   └── style.css          # CSS for the web app
├── README.md              # This file
🚀 How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install dependencies:

bash
Copy
Edit
pip install flask
Run the app:

bash
Copy
Edit
python app.py
Open your browser and go to:
👉 http://127.0.0.1:5000

✍️ How to Use
On the home page, enter symptoms separated by commas (e.g. fever, cough, fatigue)

The app will suggest possible diseases based on the symptoms

Click “View Patient History” to see all previous diagnosis records

🧠 Knowledge Base
The system includes rules for diseases like:

Common Cold

Flu

COVID-19

Pneumonia

Dengue

Asthma
…and more!

You can extend the self.diseases dictionary in app.py to add more.

📓 History
All diagnoses are stored in history.json with:

Timestamp

Symptoms entered

Diagnosis result

Probability score

🛠️ Notes
CSS must be located in the static folder.

HTML templates should be inside templates.
