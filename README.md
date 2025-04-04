# **Team 6 HERE Chicago Hackathon**

**Problem**
Assessing whether a WSIGN406 error (Motorway sign is associated to a road that has a range for Pedestrian = TRUE within 20m distance or its associated road is outside the range of 20m) is caused by 1 of 4 scenarios:
1. Sign no longer exists
2. Sign exists but is associated with the wrong road
3. Sign exists and is associated with the right road, but the “PEDESTRIAN == TRUE” attribute is wrong
4. Legitimate Exception
Communicating results in an intuitive manner


**Our Solution**

Our solution utilizes the provided GeoJSON data and displays the results using HERE Maps API with Javascript and color-coded map points.
Our approach:
1. Determine if the sign exists based on confidence score of "EXISTENCE" and "obervationCounts" attributes (Scenario 1)
If the sign exist:
2. Calculate distance of nearby roads to identify and store the topology within 20 meters of the sign 
3. We will decide our sign falls in which part of the topology and use GeoJSON in topology to determine if it is motorway. ALso record the pedestrian attribute.
Based on is motorway and pedestrian attribute.
- If the associated road is a motorway, it is identitfied as Scenario 3.
- If the associated road is out of 20m radius and/or not a motorway, it may be associated with the wrong road​.
- If the sign is associated with the wrong road and there is a nearby motorway, it is identified as Scenario 2.
- If no nearby motorway is found and none of the previous cases apply, it is identified as Scenario 4.


**Environment Setup**

1. Clone repository
2. To install necessary packages, run
```
pip3 install pandas flask flask-cors
```
and
```
brew install node
```
3. 


**Instructions**
1. In your terminal, run
2. To start the Flask application, run
```
python3 points.py
```
3. Open a *separate* terminal, run
```
npx http-server
```
4. Navigate to http://localhost:8080/map.html to see the results!
The map's pin colors correlate to the number scenario the WSIGN406 error has been identified with.
- Red: Scenario 1
- Blue: Scenario 2
- Green: Scenario 3
- Purple: Scenario 4
