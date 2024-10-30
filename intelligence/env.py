import agentspeak.stdlib
import agentspeak.runtime
import joblib
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import pickle
import os


# Load the Random Forest model
model = joblib.load('intelligence/config/random_forest_model.pkl')

# Load the encoders
with open('intelligence/config/gender_encoder.pkl', 'rb') as f:
    gender_encoder = pickle.load(f)
with open('intelligence/config/occupation_encoder.pkl', 'rb') as f:
    occupation_encoder = pickle.load(f)
with open('intelligence/config/bmi_encoder.pkl', 'rb') as f:
    bmi_encoder = pickle.load(f)
with open('intelligence/config/bp_encoder.pkl', 'rb') as f:
    bp_encoder = pickle.load(f)
with open('intelligence/config/sd_encoder.pkl', 'rb') as f:
    sd_encoder = pickle.load(f)

# Load the scaler
with open('intelligence/config/scaler.pkl', 'rb') as f:
    loaded_scaler = pickle.load(f)

# Register the function in agentspeak
actions = agentspeak.Actions(agentspeak.stdlib.actions)

# Function to generate simulated basic data
def generate_data():
    gender = random.choice(['Male', 'Female'])
    age = random.randint(18, 65)
    occupation = random.choice(['Software Engineer', 'Doctor', 'Sales Representative', 'Teacher', 'Engineer', 
                               'Accountant', 'Lawyer', 'Nurse', 'Scientist', 'Salesperson'])
    bmi = random.choice(['Normal Weight', 'Normal', 'Overweight', 'Obese'])
    blood_pressure = random.choice(['Normal','Elevated', 'Hypertension Stage 1', 'Hypertension Stage 2'])
    heart_rate = random.randint(60, 100)
    steps = random.randint(3000, 15000)
    disorder = random.choice(['None', 'Sleep Apnea', 'Insomnia'])
    return gender, age, occupation, bmi, blood_pressure, heart_rate, steps, disorder

# Function to simulate a full day of the person agent
@actions.add_function(".get_data",(str))
def get_data(cadena):
    gender, age, occupation, bmi, blood_pressure, heart_rate, steps, disorder = generate_data()
    sleep_duration = round(random.uniform(4, 10), 1)  # Sleep duration in hours
    sleep_quality = random.randint(1, 10)   # Sleep quality
    activity_level = random.randint(30, 90)  # Physical activity
    stress_level = random.randint(1, 10)  # Stress level (1-10)
    return f"{gender};{age};{occupation};{sleep_duration};{sleep_quality};{activity_level};{stress_level};{bmi};{blood_pressure};{heart_rate};{steps};{disorder}"


# Prediction function with all variables
@actions.add_function(".make_prediction",(str))
def make_prediction(string):
    # Split the string by semicolons
    data = string.split(';')
    # Create the dictionary
    data_dict = {
        'Person ID': 99,
        'Gender': [data[0].strip()], 
        'Age': [int(data[1])],  
        'Occupation': [data[2]],
        'Sleep Duration': [float(data[3])],  
        'Quality of Sleep': [int(data[4])], 
        'Physical Activity Level': [int(data[5])],  
        'Stress Level': [int(data[6])],  
        'BMI Category': [data[7]],
        'Blood Pressure': [data[8]],
        'Heart Rate': [int(data[9])],  
        'Daily Steps': [int(data[10])],  
        'Sleep Disorder': [data[11]]
    }
    df = pd.DataFrame(data_dict)
    
    # Standardize variables
    std_columns = df[['Age', 'Sleep Duration', 'Physical Activity Level', 'Stress Level', 'Heart Rate', 'Daily Steps']].columns
    df[std_columns] = loaded_scaler.transform(df[std_columns])

    # Apply LabelEncoder to the categorical columns
    df['Gender'] = gender_encoder.transform(df['Gender'])
    df['Occupation'] = occupation_encoder.transform(df['Occupation'])
    df['BMI Category'] = bmi_encoder.transform(df['BMI Category'])
    df['Blood Pressure'] = bp_encoder.transform(df['Blood Pressure'])
    df['Sleep Disorder'] = sd_encoder.transform(df['Sleep Disorder'])

    # Dropping the 'weak correlations'
    df.drop(labels=['Gender', 'Occupation', 'Physical Activity Level', 'Blood Pressure', 'Daily Steps', 'Quality of Sleep'], axis=1, inplace=True)

    prediction = model.predict(df)[0]
    return int(prediction)


for day in range(5):  # Simulate 5 days
    print(f"\nSimulation {day + 1}:")

    # Create the agent environment
    env = agentspeak.runtime.Environment()

    # Load the agents
    with open(os.path.join(os.path.dirname(__file__), "person.asl")) as source:
        person = env.build_agent(source, actions)
    with open(os.path.join(os.path.dirname(__file__), "wearable.asl")) as source:
        wearable = env.build_agent(source, actions)
    with open(os.path.join(os.path.dirname(__file__), "server.asl")) as source:
        server = env.build_agent(source, actions)
    with open(os.path.join(os.path.dirname(__file__), "virtual_doctor.asl")) as source:
        virtual_doctor = env.build_agent(source, actions)

    # Run the agents (maintain the current order)
    env.run()