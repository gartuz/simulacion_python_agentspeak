# BDI Agent-Based Sleep Quality Simulation

This project simulates the interaction between a person, a wearable device, a virtual doctor, and a server to assess and improve sleep quality using a Belief-Desire-Intention (BDI) agent framework.

## Project Structure
   
![Files](./images/files.png)

* **intelligence:** Contains the Python code for the BDI agent simulation.
    * **config:** Stores configuration files and trained machine learning models.
    * **env.py:** Sets up the simulation environment and runs the simulation.
    * **\*.asl:**  Files defining the behavior of each agent (person, server, virtual doctor, wearable).
* **images:** Contains an image illustrating the simulation flow.


## How to Run

1. **Navigate to the project's root directory.** Make sure you are **outside** the `intelligence` folder.
2. **Execute the simulation:**
   ```bash
   pip install -r requirements.txt
   python3 ./intelligence/env.py
   
* **Flow's Diagram.**
   
![Flows Diagram](./images/flow.png)
