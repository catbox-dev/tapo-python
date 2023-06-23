# Unofficial Tapo REST API with OpenAI GPT-3 integration

This program exposes a REST API with OpenAI GPT-3 integration to change the color of your Tapo devices (light bulbs, strips, etc.) based on the impact of a cybersecurity alert.

It is based on the [unofficial Tapo API](https://crates.io/crates/tapo) and the [OpenAI GPT-3 API](https://beta.openai.com/).

## Table of Contents

* [Configuration](#configuration)
* [Usage](#usage)
* [Credits](#credits)

## Configuration

1. Create a Tapo account and add your Tapo devices to it from the phone app.
2. Create an OpenAI account and get your API key from [here](https://beta.openai.com/account/api-keys).
3. Open the terminal application on your computer.
4. Clone the repo
```sh
git clone https://github.com/catbox-dev/tapo-python.git
```

5. Access to the GitHub directory
```sh
cd path/to/tapo-rest
```

6. Install the tapo-rest program by [Clément Nerma](https://github.com/ClementNerma/tapo-rest)
```sh
cargo install --git https://github.com/ClementNerma/tapo-rest
```

7. Without closing the terminal, modify the configuration file `config.json` with your Tapo credentials and your OpenAI API key
```json
{
    "account": {
        "username": "<your tapo account's email>",
        "password": "<your tapo account's password>",
        "openAI_token": "<your openAI token>"
    },
    "devices": [
        {
            "name": "<name of the device>",
            "device_type": "<model of the device>",
            "ip_addr": "<ip address of the device>",
            "port": "<port of the device>"
        }
    ]
}
```

We recommend to use the default port `9999` for the Tapo devices (for this README we will use this port, but you can choose any port you like).
The ip address of the device can be found in the Tapo app by clicking on the device and then on the settings icon in the top right corner.

e.g.:
```json
{
    "account": {
        "username": "example@email.com",
        "password": "example_password",
        "openAI_token": "example_token"
    },
    "devices": [
        {
            "name": "mytapo",
            "device_type": "L900",
            "ip_addr": "123.123.123.123",
            "port": "9999"
        }
    ]
}
```

The `name` field can be anything you want.  
The `device_type` field can be any of:

* `L510`
* `L530`
* `L610`
* `L630`
* `L900`
* `L920`
* `L930`
* `P100`
* `P105`
* `P110`
* `P115`

8. Run the server (with the default port `9999` but you can choose whatever port you want)
```sh
cargo run -- --devices-config-path config.json --port 9999 --auth-password 'potatoes'
```

This will run the server on `0.0.0.0:9999` (you can chose any port you like).

**IMPORTANT:** Do not close the terminal, otherwise the server will stop.

## Usage

1. Open the terminal application on your computer, without closing the terminal where you ran the server.
2. Access to the GitHub directory
```sh
cd path/to/tapo-rest
```

3. Run the python script
```sh
python3 main.py
```

## Credits

* This is a fork of the project [tapo-rest](https://github.com/ClementNerma/tapo-rest) by [Clément Nerma](https://github.com/ClementNerma)
* OpenAI GPT-3 integration by [Pedro Castañeda](https://github.com/catbox-dev)
