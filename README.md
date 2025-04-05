# **Team 6 HERE Chicago Hackathon**

## **Problem**
Assessing whether a WSIGN406 error (Motorway sign is associated to a road that has a range for Pedestrian = TRUE within 20m distance or its associated road is outside the range of 20m) is caused by 1 of 4 scenarios:
1. Sign no longer exists
2. Sign exists but is associated with the wrong road
3. Sign exists and is associated with the right road, but the “PEDESTRIAN == TRUE” attribute is wrong
4. Legitimate Exception


## **Our Solution**
*See more details in our presentation [here](https://docs.google.com/presentation/d/17yF1xy4OnIflHMS86F4-_w6f35uXtHyCLkViw6w1OWM/edit?usp=sharing).*

We utilize HERE's GeoJSON data to create testing conditions to identify which Scenario the WSIGN406 error falls under and then determine which changes need to be made (if necessary). Using Python Flask to handle backend data processing, we serve our results to an HTML/JavaScript frontend that leverages the HERE Maps API. The data is visualized with color-coded map points to create an intuitive and visually engaging user interface.

**Our approach**:
1. Determine if the sign exists based on confidence score of "EXISTENCE" and "obervationCounts" attributes (Scenario 1)

If the sign exists:

3. Calculate distance of nearby roads using the Harversine distance formula to identify the topology within 20 meters of the sign 

4. Using the "isMotorway" and "pedestrian" topology attributes, we identified Scenarios 2-4 using the following conditions:
  - If the associated road is a motorway, it is identitfied as Scenario 3.
  - If the associated road is out of 20m radius and/or not a motorway, it may be associated with the wrong road​.
    - If the sign is associated with the wrong road and there is a nearby motorway, it is identified as Scenario 2.
  - If no nearby motorway is found and none of the previous cases apply, it is identified as Scenario 4.

<img width="1512" alt="Screenshot 2025-04-04 at 2 10 37 PM" src="https://github.com/user-attachments/assets/c668766c-bc99-4eb8-b38b-a7a8063f5fa6" />



## **Environment Setup**

1. Clone repository
2. To install necessary packages, run
```
pip3 install pandas flask flask-cors numpy
```
*Note: Use pip3 instead of pip if using Python 3.*

3. Install Node.js [here](https://nodejs.org/en). Alternatively, if you have Homebrew installed, run
```
brew install node
```

## **Instructions**

1. To start the Flask application, run
```
python3 points.py
```
2. In a *__separate__* terminal, run
```
npx http-server
```
4. Navigate to http://localhost:8080/map.html in your browser to see the results!
The map's pin colors correlate to the number scenario the WSIGN406 error has been identified with.
- Red: Scenario 1
- Blue: Scenario 2
- Green: Scenario 3
- Purple: Scenario 4
