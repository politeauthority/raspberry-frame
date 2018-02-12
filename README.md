# Raspberry-Frame
Raspberry Pi picture frame system.
```
docker build -t raspberry-frame --no-cache .

docker run \
    --name rf \
    -link some-precona:mysql \
    -e RF_MYSQL_USER='user' \
    -e RF_MYSQL_PASS='password' \
    -e INSTAGRAM_CLIENT_ID = "client id" \
    -e INSTAGRAM_CLIENT_SECRET = "client secret" \
    -e INSTAGRAM_TOKEN = "toen" \
    -v /Users/alix/Data/raspberry-frame:/data/ \
    -v /Users/alix/repos/raspberry-frame:/opt/raspberry-frame \
    -p 5001:80 \
    -td \
    raspberry-frame:latest
```
