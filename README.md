## Target IP Web Application Info
Application designed due to target IP address geolocation data. 
Application has postgres database attached.

Authentication method: JWT Tokens

Geolocation API: https://api.ipstack.com/

## Endpoints allowed

Not protected [POST] "/login"

Protected [GET] "/get_ip_location/{ip_address}"

Protected [POST] "/add_ip_location"

Protected [DELETE] "/delete_ip_location"

Full documentation attached in Postman

## Addictional services

pgadmin databse GUI hosted on port 5050