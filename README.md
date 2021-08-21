# LeaguePredictor
MSc Dissertation Project - for the creation of an Alexa Skill that can be utilised to predict the outcome of a League of Legends game. 

This project utilised various APIs, most notably of which being the League of Legends (Riot API). In addition to exploring the application of the python programming language and accompanying machine leanring libraries and resources such as, Pandas, Scikit-learn, and numpy.

Overall, the Alexa device was found to be ill-fitting fro this kind of functionality due to Riot Games - the creators of League of Legends, not allowing for third party connections to be authorised, therefore OAuth could not be used. This made the interlinking between accounts and the device quite rigid. 

However, the trained model was able to determine the outcome of League of Legends games with a rate of 60% accuracy, given the utilised dataset and the depth to these kinds of games this was deemed to be a moderate success. 

## Technology Used
- AWS Lambda
- Dynamo DB
- S3 File Storage
- Alexa Skills Kit
- Cassiopeia (Python Riot API Wrapper)
- SciKit Learn
- Pandas - Numpy

## Visual Structure of the System

<p align="center"><img src="https://i.imgur.com/NGHtWrv.png" 
alt="Skill Structure"/></p>

## Video Demonstration

<p align="center">
  <a href="https://drive.google.com/file/d/1lpM9OnSK7DZSgdNf4pfEG3dmH_QnI38a/view?usp=sharing" target="_blank" title="LeaguePredictor">
    <img src="https://i.imgur.com/IovIoQh.png" alt="LeaguePredictor Video" width="400" height="240" border="10"/>
  </a>
</p>
