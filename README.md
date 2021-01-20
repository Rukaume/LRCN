LRCN for behavioral phenotype
==
These scripts enable you to predict an animal behavioral phenotype. For example, if you want to detect a quiescent state, the trained model returns the prediction data. 

## Description

## Workflow
(Training)

1. Prep video 

2. Extract images from video (run Image_prep.py)  

3. Annotation by python video annotator or ImageJ and make .csv file

4. .npy file prep (run Data_prep.py)

5. upload those files to Google drive

6. run LRCN.ipynb on Google colab. (with GPU)


(Prediction)

7. download .m5 file (model.m5) 

8. prep video files

9. prediction (main1.py)

Output is .csv file (jump time)

(Annotated video make) 

10. make annotated video (Annotatedvideo2.py)



## Requirement

## Usage

## Licence

[MIT]

## Author

[Rukaume]
