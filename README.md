# Active Learning for Tweet Sentiment Classification



To Do:

- showing new tweet without refreshing the page --> https://stackoverflow.com/questions/22577457/update-data-on-a-page-without-refreshing
- Visualize progress during training & show when training is finished
- Discuss how to handle not preannotated datasets (.sentiment is sometimes used (would throw an error right now))
- bisheriges Modell: tiny-bet (prajjwal1/bert-tiny) --> kann nur binary Classification (hier muss man noch manuell ein Outputlayer hinzufügen für mutinomiale Klassifikation), also this should be done in the constructor 
-  We need to figure out if we want to compartmentalize the modelling process further by i.e. making a whole model class (i guess just to add an appropriate output layer this wont be needed, but if we want to use ensemble stuff and/or more sophisticated models it could make sense)
- Warnings when no new labels - dataset is fully labeled