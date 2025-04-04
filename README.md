# **Team 6 HERE Chicago Hackathon**

**Problem**

**Our Solution**

Our solution utilizes the provided GeoJSON data.
Our approach:
1. Determine if the sign exists based on confidence score of "EXISTENCE" and "obervationCounts" attributes (Scenario 1)
If the sign exist:
2. Calculate distance of nearby roads to identify and store the topology within 20 meters of the sign 
3. We will decide our sign falls in which part of the topology and use GeoJSON in topology to determine if it is motorway. ALso record the pedestrian attribute.
Based on is motorway and pedestrian attribute.
if asscoiated road is out of 20 meters radius. It is associated with the wrong road​.
If asscoiated is motorway, it is Case 3, correct association, incorrect road attribution. 
if asscoiated is not motorway,it is associated with the wrong road​.
if associated with the wrong road, we will choose a motorway near the sign as the corrected assications. Case 2.
if none nearby motorway is found. It is case 4.


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
4. Navigate to \url{http://localhost:8080/map.html}.
