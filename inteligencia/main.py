import agentspeak.stdlib

import agentspeak.runtime

import joblib

import pandas as pd

import random

from sklearn.preprocessing import StandardScaler

from sklearn.preprocessing import LabelEncoder

import pickle

import os

import random



# Cargar el modelo Random Forest

modelo = joblib.load('inteligencia/config/random_forest_model.pkl')

# Cargar los encoder

with open('inteligencia/config/gender_encoder.pkl', 'rb') as f:

    gender_encoder = pickle.load(f)

with open('inteligencia/config/occupation_encoder.pkl', 'rb') as f:

    occupation_encoder = pickle.load(f)

with open('inteligencia/config/bmi_encoder.pkl', 'rb') as f:

    bmi_encoder = pickle.load(f)


with open('inteligencia/config/bp_encoder.pkl', 'rb') as f:

    bp_encoder = pickle.load(f)

with open('inteligencia/config/sd_encoder.pkl', 'rb') as f:

    sd_encoder = pickle.load(f)

# Cargar el scaler

with open('inteligencia/config/scaler.pkl', 'rb') as f:

    loaded_scaler = pickle.load(f)
    

# Registrar la función en agentspeak

actions = agentspeak.Actions(agentspeak.stdlib.actions)


# Función para generar datos básicos simulados

def generar_datos():

    genero = random.choice(['Male', 'Female'])

    edad = random.randint(18, 65)

    ocupacion = random.choice(['Software Engineer', 'Doctor', 'Sales Representative', 'Teacher', 'Engineer', 'Accountant', 'Lawyer', 'Nurse', 'Scientist', 'Salesperson'])

    bmi = random.choice(['Normal Weight', 'Normal', 'Overweight', 'Obese'])

    pa = random.choice(['Normal','Elevated', 'Hypertension Stage 1', 'Hypertension Stage 2'])

    fc = random.randint(60, 100)

    pasos = random.randint(3000, 15000)

    trastorno = random.choice(['None', 'Sleep Apnea', 'Insomnia'])

    return genero, edad, ocupacion, bmi, pa, fc, pasos, trastorno



# Función para simular un día completo del agente persona

@actions.add_function(".get_data",(str))

def get_data(cadena):

    genero, edad, ocupacion, bmi, pa, fc, pasos, trastorno = generar_datos()

    horas_sueno = round(random.uniform(4, 10), 1)  # Duración del sueño en horas

    calidad_suenio = random.randint(1, 10)   # Calidad del sueño

    nivel_actividad = random.randint(30, 90)  # Actividad física

    nivel_estres = random.randint(1, 10)  # Nivel de estrés (1-10)

    return ""+ genero + ";" + str(edad) + ";" + ocupacion + ";" + str(horas_sueno) + ";" + str(calidad_suenio) + ";" + str(nivel_actividad) + ";"  + str(nivel_estres) + ";" + str(bmi) + ";" + str(pa) + ";" + str(fc) + ";" + str(pasos) + ";" +  trastorno +  ""
    
    # Update the agent's beliefs using test_beliefsome_goal(M)

     # Actualizar las creencias del agente


    #return {"genero": genero, "edad": edad, "ocupacion": ocupacion, "bmi": bmi, "pa": pa, "fc": fc, "pasos": pasos, "trastorno": trastorno, "horas_sueno": horas_sueno, "calidad_suenio": calidad_suenio, "nivel_actividad": nivel_actividad, "nivel_estres": nivel_estres}



# Simular varios días

# Función de predicción con todas las variables

@actions.add_function(".hacer_prediccion",(str))
def hacer_prediccion(cadena):

    # Split the string by semicolons
    data = cadena.split(';')

    # Create the dictionary
    datos = {
        'Person ID': 99,
        'Gender': [data[0].strip()],  # Use strip() to remove leading/trailing spaces
        'Age': [int(data[1])],  # Convert age to integer
        'Occupation': [data[2]],
        'Sleep Duration': [float(data[3])],
        'Quality of Sleep': [int(data[4])],
        'Physical Activity Level': [int(data[5])],  # Convert Physical Activity Level to integer
        'Stress Level': [int(data[6])],  # Convert daily steps to integer
        'BMI Category': [data[7]],
        'Blood Pressure': [data[8]],
        'Heart Rate': [int(data[9])],  # Convert stress level to integer
        'Daily Steps': [int(data[10])],  # Convert sleep duration to integer
        'Sleep Disorder': [data[11]]
    }

    df = pd.DataFrame(datos)
    
    # Standarize Variables

    #scaler = StandardScaler()

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

    prediccion = modelo.predict(df)[0]
    x = int(prediccion)
    return x


for dia in range(5):  # Simular 5 días

    print(f"\nSimulacion {dia + 1}:")

    # Crear el entorno de agentes

    env = agentspeak.runtime.Environment()



    # Cargar los agentes

    with open(os.path.join(os.path.dirname(__file__), "persona.asl")) as source:

        persona = env.build_agent(source, actions)

    with open(os.path.join(os.path.dirname(__file__), "wearable.asl")) as source:

        wearable = env.build_agent(source, actions)
    with open(os.path.join(os.path.dirname(__file__), "servidor.asl")) as source:

        servidor = env.build_agent(source, actions)
    
    with open(os.path.join(os.path.dirname(__file__), "medico_virtual.asl")) as source:

        medico_virtual = env.build_agent(source, actions)
    


    # Ejecutar los agentes (mantener el orden actual)
    env.run()