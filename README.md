# Controvercy detector.
 
My AI model will try to address this issue of controversies which can have a serious negative impact.

It provides a possible solution to detect or predict such malicious controversies and alert authorities in advance to take the necessary steps to stop any unfortunate event.

It will use Geo-Location to track down perpetrators who started it and the regions where it can have a serious impact.

The Project is built in two Phases:

### Phase 1:

Uses Twitter API to show the demo of how it will detect malicious controversies based on trending topics and user tweets on topics.

It will classify those tweets as either Positive or Negative and based on that calculate Controversy Rate(CR). IF the CR >= 40% then the topic, its related tweets, Geo-Location of users, and username will be shortlisted and saved in a CSV file for further analysis.


### Phase 2:

Is a theoretical model that will analyze the results saved in a CSV file along with the Geolocation of each user.

It will then compare the topic, the related crime that happened in that Geolocation as well as the main motivation behind those crimes.

If all this is in synch with topics shortlisted in Phase 1 then such topics will be flagged as controversial and the system will alert authorities along with necessary data.

## Twitter API

I used twitter API to fetch the real time tweets based on each current topic.


#### Note:
I created a list of trending topics based on the date on which I gave my presentation on progress of my model
