# Python Search Engine

## Preview
![Python Search Engine](https://raw.githubusercontent.com/manuelro/python-search-engine/master/assets/search-engine.gif)

## What does the app do?
This little search engine allows you to perform searches on Google using Google's Custom Search Engine and will save logs (activity logs) to a MongoDB and will post these logs to the Slack API.

## Why did you create this?
Just for fun, but hopefully this will serve as a basis for a more complex integration project that can mix frontend and backend technologies.

## Running the script
The scripts needs some information (ids, external api keys) to work. In order to run the server do the following:
- Download the repo to you computer
- Make sure to have Python 2.7 or greater installed in your system
- cd to the folder that contains the server file (./server)
- Install the required libraries (at the top of the server file)
- Run the following command:

```
python server.py --mongourl mongodb://<yourmongouser>:<thepassword>@ds153732.mlab.com:53732/<thedbname> --slackchannel <The slack channel ID> --slacktoken <The slack API token> --googlekey <Google API key> --googlecse <Google Custom Search Engine ID>
```
### Flags
Flags are passed to the app through the command line interface (CLI). All the flags are required.

#### `--mongourl`
This flag sets the mongodb URL (with username and password). I recomend using mlab.com for This.
```
--mongourl mongodb://<yourmongouser>:<thepassword>@ds153732.mlab.com:53732/<thedbname>
```

#### `--slackchannel`
This flag should contain the Slack channel id.
```
--slackchannel SDGF3S126S
```

#### `--slacktoken`
This flag should contain the Slack app token.
```
--slacktoken xoxp-210869292357-210203788401-210102158864-dd56259149e04d8478a79b426409cfc8
```

#### `--googlekey`
This flag should contain Google's API key.
```
--googlekey AIzaSyA82kj00TzSUGoL7PvJsC09vv1PLZ_-lPc
```

#### `--googlecse`
This flag should contain Google Custom Search Engine ID.
```
--googlecse 0020887974925052946331:aozogqxuyy4
```

*All the tokens and ids provided in this example have been modified for security reasons*

## Giving the app a try
The app will start running on localhost on port 5000, you can use Postman to test the API.

The server will provide you with a token with a validity of 1 minute, and a refresh token with a validity of one year.

The username is 'username' and the password is 'password'.

## API Endpoints
This project includes an API with which a frontend can interact.

### `POST /login`
In order to be able to authenticate against the server you first have to send an `Authorization` header with basic set on it: `Basic dXNlcm5hbWU6cGFzc3dvcmQ=`, pass your `username` (with value 'username') and `password` (with value 'password') to the `/login` endpoint, using the `POST` request method. The server will respond with a set of two `tokens`, one for normal consumption and another one to refresh the prior.

#### Query params
##### `username`
Set this value to be 'username'.
##### `password`
Set this value to be 'password'.

### `POST /refresh`
Send a `POST` request and pass in the refresh token via query params. The server will check if the refresh token is valid, if so, will issue another access token and respond with a set of two tokens, one for normal use and another one to refresh the prior.

#### Query params
##### `token`
The normal token.

### `POST /search`
This endpoint will allow you to perform searches by using Google Custom Search Engine API.

#### Query params
##### `cat`
This is just a category or keyword to further filter the search results.
##### `query`
This will contain the search query that is going to be passed to Google Custom Search Engine API.

### `POST /event`
This endpoint will allow you to directly send formatted messages using the Slack API. This is intended in case there is further integration with a frontend.

#### Query params
##### `thumbnail`
A thumbnail URL.
##### `description`
A description for the chat message.
##### `url`
The URL pointing to the current search result.
##### `cat`
The category of the search, just a keyword.
##### `query`
The search query.

## Token validity
There are two types of tokens, a normal token used to perform a request to the server and a refresh token, used to refresh the normal token. Tokens are intended to be saved on a local storage structure on your frontend, that way you can easily have access to them and use them to validate your identity with the server without having to send the username and password with every request.

### Normal token
The normal token has a validity of 1 minute since the moment it was generated.

### Refresh token
The refresh token has a validity of one year since the moment you generated it.

## Contributions
Feel free to contribute with any crazy idea you think can make this project even more useful for the community. Cheers!

-- Manuel Ro

---

Copyright 2017 Manuel Ro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
