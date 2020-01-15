#!/bin/sh
# AD account login
SSEAPI_URL=https://localhost
SSEAPI_AD_CONFIG_NAME=winad2 # winad2: Directory Service in SSE, internal: local accounts
SSEAPI_AD_USER=amalaguti
SSEAPI_AD_PW=salT5282

# Get initial _xsrf
curl -ik $SSEAPI_URL/account/login \
    --user '$SSEAPI_AD_USER:$SSEAPI_AD_PW' \
    --cookie-jar initial_xsrf.txt

# Authenticate with _xsrf cookie
curl --silent -k $SSEAPI_URL/account/login \
    --cookie initial_xsrf.txt \
    --cookie-jar authed_session.txt \
    --header "X-Xsrftoken: $(grep -w "_xsrf" initial_xsrf.txt | cut -f7)" \
    --data "{\"config_name\": \"$SSEAPI_AD_CONFIG_NAME\", \"username\": \"$SSEAPI_AD_USER\", \"password\": \"$SSEAPI_AD_PW\"}" \
    | jq 'del(.attributes.permissions)'

# Get version, using jq to filter out "deps" key info
curl --silent -k $SSEAPI_URL/rpc \
    --cookie authed_session.txt \
    --header "X-Xsrftoken: $(grep -w "_xsrf" initial_xsrf.txt | cut -f7)" \
    --data '{"resource": "api", "method": "get_versions"}' \
    | jq 'del(.ret.deps)'


# Using json file as payload
# --data @payload.json
# payload.json:
#{"config_name": "internal", "username": "root", "password": "salty1234"}
