# ZigBee Controller with HTTP API (ZigCoHTTP)

This python application creates a ZigBee network using [zigpy](https://github.com/zigpy/zigpy) and [bellows](https://github.com/zigpy/bellows). ZigBee devices joining this network can be controlled via a HTTP API. It was developed for a Rasperry Pi using a [Matrix Creator Board](https://www.matrix.one/products/creator) but should also work with other computers with Silicon Labs Zigbee hardware.

## Requirements

* Compatible Zigbee hardware (see https://github.com/zigpy/bellows)
* Python 3 and pip

## Installation

```
pip install -r requirements.txt
```

## Running the application
```
python main.py
```

## Running with Docker
```
docker build -t <name> .
docker run -d -p <port>:<port> --restart unless-stopped --device=/dev/<device> <name>
```

## Configuration
The following environment variables can be set:

|Name   |   Default   |  Description
|--|--|--
|PORT  |8080  |The port used by the application to listen for HTTP Requests
|DEVICE|/dev/ttyS0|ZigBee Radio Device
|DATABASE_FILE|devices.db|File to store discovered ZigBee devices


## API

`POST /permitjoin`

Allow devices to join the ZigBee network for the next 60s. Devices that have been in another ZigBee network before have to be resetted to join a new network.


`GET /devices`

Returns a json array of all devices in the network.


`POST /<device_ieee>`

```
{
  "command": "<command>",
  "params": [param1, param2, ...]
}
```
Sends a command to the device with the given `device_ieee` (unique identifier). The `device_ieee` of each device in the network can be found by calling `GET /devices`. `params` are not required for all commands and therefore optional.


## Commands
These commands can be sent in the body of a HTTP POST request to `/<device_ieee>`.
### Turn devices on or off:

```
{"command": "toggle"}
```
```
{"command": "on"}
```
```
{"command": "off"}
```

### Level Control (For example brightness of a Philips Hue lamp):

```
{
  "command": "move_to_level",
  "params": [255, 2]
}
```
Sets the brightness to 255 (between 0 and 255) in a transition time of 2s.


### Color Control (For example color of a Philips Hue lamp):

```
{
  "command": "move_to_hue_and_saturation",
  "params": [114, 50, 2]
}
```
Sets the hue to 114 and saturation to 50 in a transition time of 2s.
