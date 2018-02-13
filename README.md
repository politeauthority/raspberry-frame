# Raspberry-Frame
Raspberry Pi picture frame system.

### Simple Run Guide
```
docker build -t raspberry-frame --no-cache .

docker run \
    --name rasframe \
    --link some-percona:mysql \
    -e RF_MYSQL_USER='root' \
    -e RF_MYSQL_PASS='password' \
    -e INSTAGRAM_CLIENT_ID="client id" \
    -e INSTAGRAM_CLIENT_SECRET="client secret" \
    -e INSTAGRAM_TOKEN="token" \
    -v /home/alix/data/raspberry-frame:/data/ \
    -v /home/alix/repos/raspberry-frame:/opt/raspberry-frame \
    -p 5001:80 \
    -td \
    rasframe
```
