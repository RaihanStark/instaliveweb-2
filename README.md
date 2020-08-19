# InstaLiveWeb

> InstaLiveWeb is a Python Flask webapp that create a Instagram Live and provide you a rtmp server and stream key to streaming using sofwares like OBS-Studio.

![login page v1](login.png)

![dashboard v1](dashboard.png)

## Features

- Start and Stop Broadcast
- Refresh Stream Key
- Display Viewers
- Display Live Comments

## Upcoming Features

- [ ] Storing and Loading Cookies
- [ ] Proxy Support
- [ ] Multi Accounts
- [ ] ??? (You decide by creating an Issues)

## Installation

#### > Clone this repo

```sh
git clone https://github.com/RaihanStark/instaliveweb.git
cd instaliveweb/
```

#### > Installing and activating the virtual environment

```sh
python -m venv env
env\Scripts\activate.bat
```

#### > Installing Packages

```sh
pip install -r requirements.txt
```

## Running on Local

```sh
set FLASK_ENV=development
flask run
```

## Author

##### HarryPython - [itsagramlive](https://github.com/harrypython/itsagramlive) ( CLI Version )

##### Raihan Yudo Saputra - [instaliveweb](https://github.com/RaihanStark/instaliveweb) ( Web Version - this repo)

> Distributed under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license. See `LICENSE` for more information.

## Contributing

1. Fork it (<https://github.com/RaihanStark/instaliveweb/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
