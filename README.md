# **Team 6 HERE Chicago Hackathon**

**Problem**

**Our Solution**

Our solution is based one geojson's data. OUr approach is:
Determine the Sign exsitance based on existing confidence score and obervation score(obervation/possible obervation times).
If the sign exist:
We will compute the topology nearby within 20 meters of the sign and store them as potential topology. 
We will decide our sign falls in which part of the topology and use geojson in topology to determine if it is motorway. ALso record the pedestrian attribute.
Based on is motorway and pedestrian attribute.
if asscoiated road is out of 20 meters radius. It is associated with the wrong road​.
If asscoiated is motorway, it is Case 3, correct association, incorrect road attribution. 
if asscoiated is not motorway,it is associated with the wrong road​.
if associated with the wrong road, we will choose a motorway near the sign as the corrected assications. Case 2.
if none nearby motorway is found. It is case 4.


**Environment Setup**


**Instructions**
