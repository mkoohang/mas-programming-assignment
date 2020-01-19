# National Parks API
This is a backend API for accessing and favoriting national parks from the National Park Services API.

# Features
- User Authentication
- JWT Token Authentication
- Favoriting parks

## Tech Stack
- Flask (Python)
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
 - Headers
```
Authorization: <api_token>
```
 - Return
```
{
    "parks": [
        <list_of_all_parks>
    ]
}
```

### Add Park (Pending)
`POST {base_url}/rest/addpark`
- In progress

### Remove Park (Pending)
`POST {base_url}/rest/removepark`
- In progress

### User (Pending)
`GET {base_url}/rest/user`
 - In progress