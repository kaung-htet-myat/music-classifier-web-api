# Music Genre Classifier Web Server with Django

A simple Django web server to serve music genre classifier. Model training is implemented in https://github.com/kaung-htet-myat/music-classifier-training-api.   
   
The server provide following functionalities:
- User account management and authentications
![login](assets/login.png)
- Classify genre of the uploaded music file
![upload](assets/file_upload.png)
![inference](assets/file_inference.png)
- Classify genre of the live streaming music from microphone
![stream](assets/streaming.png)
- Checking the file inference history
![history](assets/history.png)