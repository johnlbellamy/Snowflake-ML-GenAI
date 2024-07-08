#bin/bash
sudo docker run -p 8080:5000 \
 -e USER_NAME=${USER_NAME} \
 -e PASSWORD=${PASSWORD} \
 -e ACCOUNT=${ACCOUNT} \
 johnb340/xgboost-wine-snowflake:v1
