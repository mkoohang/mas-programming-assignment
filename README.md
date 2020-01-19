# National Parks API
This is a backend API for accessing and favoriting national parks from the National Park Services API.

## Tech Stack
- Python
- MongoDB

## Endpoints

base_url = https://powerful-wildwood-07865.herokuapp.com/

### Registration
`POST {base_url}/rest/register`
- This is where you can register users with the service.
- Body
```
{ 
    "username": <username>, 
    "password": <password> 
}
```
 - Return
```
{
    "message": "New user <username> created!",
    "token": <api token>
}
```

### Login
`POST {base_url}/rest/login`
- This is where you can log in to the service.
- Body
```
{
    "username": <username>,
    "password": <password>
}
```

 - Return
```
{
    "message": "Login successful!",
    "token": <api_token>
}
```

### All Parks
`GET {base_url}/rest/allparks`
- This is where you can view all parks.
- Body
```
{
    "username": <username>,
    "password": <password>
}
```

 - Headers
```
Authorization: <api_token>
```
 - Return
```
{
    "parks": [<list_of_all_parks>]
}
```

### Add Park
`POST {base_url}/rest/addpark`
- Body
```
{
    "username": <username>,
    "password": <password>
}
```
 - Headers
```
Authorization: <api_token>
```
 - Return
```
{
    "park": {
        <details_of_park_added>
    },
    "wishlist": [<list_of_parks>]
}
```

### Remove Park
`POST {base_url}/rest/removepark`
- Body
```
{
    "~~username~~": <username>,
    "password": <password>
}
```
 - Headers
```
Authorization: <api_token>
```
 - Return
```
{
    "park": {
        <details_of_park_removed>
    },
    "wishlist": [<list_of_parks>]
}
```

### User
`GET {base_url}/rest/user`
 - Headers
```
Authorization: <api_token>
```
 - Return
```
{
    "username": <username>,
    "id": <id>,
    "wishlist": [<list_of_parks>]
}
```