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

## Giving the app a try
The app will start running on localhost on port 5000, you can use Postman to test the API.

The server will provide you with a token with a validity of 1 minute, and a refresh token with a validity of one year.

The username is 'username' and the password is 'password'.

## API Endpoints
Coming soon...
