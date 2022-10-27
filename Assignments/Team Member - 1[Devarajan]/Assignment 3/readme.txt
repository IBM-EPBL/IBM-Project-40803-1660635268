Name : DEVARAJAN P
Reg No:713919106006
College Name:Sri Ranganathar Institute Of Engineering and technology
Descprition:
    Assignment 3 (To include cloud object storage,watson assistant)

Assignment Tasks:


Task 1:created a bucket in cloud object storage 

Task 2:Uploaded images from flask server and can be viewed
        "/upload"-This Route can upload the files to cloud object storage and the user should enter the bucket name,filename,filename
        "/user" -This Route can display the uploaded images

Task 3:Uploaded a css file from local storage to cloud object storage and this file is applied to an html page 
        "/cssupload"-Routes used to upload a css file to cloud
        "/csspage"  -Route used to view the html page where the css file is returned from the cloud and the css is applied to the page

Task 4:created an watson assistant for to find the branches of the hospital 
        ChatBot URl : https://web-chat.global.assistant.watson.appdomain.cloud/preview.html?backgroundImageURL=https%3A%2F%2Feu-gb.assistant.watson.cloud.ibm.com%2Fpublic%2Fimages%2Fupx-6a20838c-920a-4d9b-903b-316e333aff13%3A%3A5493d50f-0e5a-4da8-9ce0-92c55911ada9&integrationID=a93cf08c-cf77-4717-81f0-fa1372122f77&region=eu-gb&serviceInstanceID=6a20838c-920a-4d9b-903b-316e333aff13

Task 5:created a watson assistant service which includes 10 steps and 3 conditions
        "/bot" - Route where the assistant is included in the httml page

//TO RUN SERVER : flask --debug run 
//Note: The connection string of (Cloud Object Storage) is removed to avoid the usage of unauthorised people.
