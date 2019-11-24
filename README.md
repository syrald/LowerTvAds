## Problematic
In France, TV channels can broadcast up to **12 min of ads per hour** with a mean of 9 min per hour per day.
It means that, 1/6 of our time watching TV is actually watching brainwashing ads we don't really want to see, that we can't skip or we might miss a part of our emission.
Our solutions for now was to use this time to talk with his/her partner, mute the TV or switch channel. But we still hear the TV and swallow the information. They got us.
The brainwashing part is actually even more true for a part of the population: Children.
When watching cartoons, TV ads target children because it suits to the content broadcasted.

We can all agree that TV ads are not the reason we are watching TV and that they are not necessary. They also bring few problems:

- Children want what they see, and that's not free.
- You can't fully control what your child is watching.
- When watching a lot TV, ads are really repetitive.

## Purpose
This repository intend to filter the TV output to decrease the brainwashing of TV ads by **automatically lowering the TV sound when an ad is broadcast**.
This project is created and maintained by Vianney Bacoup. This is it's first Data Science project from the problematic to the solution. The original idea comes from Benoit Pimpaud who helps Vianney on every aspect of the project when needed by giving clues.

## Getting data
To save a good amount of data, I was not able to turn on the TV and record the audio because it was making too much noise and disturbed the quiet place I like to have at home. We could record only when we watch the TV, but it means that the data will only be on 2 or 3 shows and relevant for our tests.
My solution was to use website broadcasting the channels live. Because I'm French, I recorded TF1, M6 and W9, 3 french channels at different time of day/night.
I know that the data is not taken the same way.
For that, I used:

- Ubuntu 18.04
- Audacity to record the audio
- Virtual speakers so that the audio is not played from the computer and it can be played during the night
> sudo modprobe snd_aloop

I did two sessions of 2-3 days each which bring me with more than 26 hours of audio, stored as .WAV file, 44100 hz and mono.
To avoid any copyright problem, I won't share the files here but only the features I extracted.

## Prepare data
With only audio files, I also need to know when it is an ad or not.
For that, I listened to my audio files and noted in a .csv when an ad starts or ends with the appropriate timestamp. Here is few lines of this file (you can look at the file TV_ad_flag.csv to see everything)
| file_id | timestamp | pub |
|--|--|--|
| 1 | 0 | 0 |
| 1 | 386 | 1 |
| 1 | 763 | 0 |
| 1 | 1349 | 1 |
| 1 | 1512 | 0 |
| 1 | 1571 | 1 |
| 1 | 1643 | 0 |
| 1 | 1702 | 1 |
| 1 | 2003 | 0 |

- **file_id** is an id to know which file is this line for (see the file TV_files.csv)
- **timestamp** is the time in seconds since the beginning of the file
- **pub** is a Boolean and is used to know when an ad starts.

With those files I have all the data I need for my problem.
I'm using **Python** with **Pandas** and **Numpy** to browse the .csv files, and **librosa** to extract features from audio files.
From the files I mentioned earlier, I did several actions:
- I fill the missing lines between the beginning of an ad and the end of the ad and vice versa)
- I attached a 10 seconds sequence from the audio file to each line in my **DataFrame**. I added a padding of "0" to avoid boundaries problems.
- I changed the "pub" variable to store the percentage of ads in the corresponding sequence. For example if the ad starts at 6 seconds in the sequence, the result is 0.4

My data in Python now looks like this:
| file_id | timestamp | pub | audioSequence |
|--|--|--|--|
| 1 | 0 | 0 |[-10;0]|
| 1 | 1 | 0 |[-9;1]|
| 1 | ... | ... |...|
| 1 | 385 | 0 |[375;385]|
| 1 | 386 | 0.1 |[376;386]|
| 1 | 387 | 0.2 |[-377;387]|
| 1 | 388 | 0.3 |[-378;388]|
| 1 | ... | ... |...|
| 1 | 761 | 1 |[751;761]|
| 1 | 762 | 1 |[752;762]|
| 1 | 763 | 0.9 |[753;763]|
| 1 | 764 | 0.8 |[754;764]|
| 1 | 765 | 0.7 |[755;765]|
| 1 | ... | ... |...|

## Extract Features
I'm using **librosa** to extract features from audio files.
My experiments with feature engineering never used audio files.
[1] & [2] helps a lot and I extracted two kind of features:
- [MFCC](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum): I extract 80 MFCC features from each 10 seconds sequences.
- [Decibels](https://en.wikipedia.org/wiki/Decibel): I extract 10 Decibels features from each 10 seconds sequences. They represent the Decibel mean of each individual second.

My final DataFrame looks like this:
| file_id | timestamp | pub | mfcc_0 | ... | mfcc_80 | db_0 | ... | db_9 |
|--|--|--|--|--|--|--|--|--|
| 1 | 0 | 0 | -688.73 | ... | 5.85 | -100.00 | ... | -41.04 |
| 1 | 1 | 0 | -611.98 | ... | 14.32 | -100.00 | ... | -45.47 |
| 1 |...|...|...|...|...|...|...|...|
| 1 | 385 | 0 | -342.31 | ... | 27.21 | -48.45 | ... | -57.12 |
| 1 | 386 | 0.1 | -360.05 | ... | -15.32 | -43.71 | ... | -78.41 |
| 1 | 387 | 0.2 | -364.44 | ... | -78.89 | -37.19 | ... | -87.56 |
| 1 | 388 | 0.3 | -353.02 | ... | 1.15 | -39.78 | ... | -82.79 |
| 1 | ... | ... |...|...|...|...|...|...|
| 1 | 761 | 1 | -320.25 | ... | 12.12 | -87.45 | ... | -78.46 |
| 1 | 762 | 1 | 14.87 | ... | 14.56 | -84.12 | ... | -75.46 |
| 1 | 763 | 0.9 | 56.42 | ... | -15.27 | -81.49 | ... | -48.12 |
| 1 | 764 | 0.8 | -158.88 | ... | -27.22 | -79.16 | ... | -49.97 |
| 1 | 765 | 0.7 | -137.13 | ... | -4.47 | -81.16 | ... | -52.79 |
| 1 | ... | ... |...|...|...|...|...|...|

Ideas of new features to try:
- Between every TV ad, there is a little silence. I think I can work on a feature like Time Since Last Silence
- I don't know a lot about audio features MFCC and Decibels. But I should try to create new features by doing an operation between them.

## Models
I created a logistic regression and a Neural Network to test my data.
The logistic regression his really fast to build. I used it to have a good and fast visualization about the features I extracted.
The Neural Network here is more appropriate for audio processing, but is more time consuming. This is the solution I choose.
I tried many different approach that you can find in the file models.py

## Split the data
With my 26 hours of audio files, I managed to have 92 624 rows.
But my problem is that only 21% of my entries are an ad. You can see in the next section how it influences the score and accuracy.
So I trained my models few different ways:
- Taking all the 92 624 rows with 21% ads.
- Reduce the amount of "not an ad" to have 47% ads. 41 506 rows.

I split the data with 20% for the test part and 80 for the training part.
You can see the results in the next section.

## Train and test
The models in the next tables are detailed in models.py.
- 92 624 rows with 21% ads.

|\\|\|| accuracy | precision | recall | f1-score |
|--|--|--|--|--|--|--|
| model1 | \| | 93.19% | 81.04% | 89.40% | 85.01% |
| model2 | \| | 95.33% | 88.94% | 89.50% | 89.22% |
| model3 | \| | 94.96% | 86.35% | 91.07% | 88.65% |
| model4 | \| | 85.24% | 75.36% | 47.57% | 58.35% |
##
- 41 506 rows with 47% ads.

|\\|\|| accuracy | precision | recall | f1-score |
|--|--|--|--|--|--|
| model1 | \| | 95.70% | 98.26% | 92.50% | 95.29% |
| model2 | \| | 98.53% | 98.28% | 98.60% | 98.44% |
| model3 | \| | 98.37% | 97.95% | 98.60% | 98.27% |
| model4 | \| | 82.92% | 83.26% | 79.66% | 81.42% |

## Conclusion
I picked the model with the biggest recall because the worst case is to lower the sound of the TV when it is not an ad. Because there is two models with the same recall, I will go with the **model2** because it has a better precision than the model3.

## Put into practice
TODO

## Sources
[1] https://medium.com/@mikesmales/sound-classification-using-deep-learning-8bc2aa1990b7
[2] https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/
[3] https://medium.com/hugo-ferreiras-blog/confusion-matrix-and-other-metrics-in-machine-learning-894688cb1c0a
