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
Coming soon...

## Contributions
Feel free to contribute with any crazy idea you think can make this project even more useful for the community. Cheers!

-- Manuel Ro

---

Copyright 2017 Manuel Ro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
