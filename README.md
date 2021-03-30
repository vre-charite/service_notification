This repo documents the service of user management. 
### How to start the service
```
sudo docker-compose up
```

### How to use the service
```
curl --header "Content-Type: application/json"   --request POST   --data '{"sender":"abc@indocresearch.org","receiver":"tiangao0611@gmail.com", "message":"tttttttt"}'   http://10.3.9.240:5065/v1/email
{
    "result": "Email sent successfully. "
}
```


