# aioruuvigateway

An asyncio-native library for requesting data from a Ruuvi Gateway.

[![PyPI - Version](https://img.shields.io/pypi/v/aioruuvigateway.svg)](https://pypi.org/project/aioruuvigateway)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioruuvigateway.svg)](https://pypi.org/project/aioruuvigateway)

---

## Installation

Requires Python 3.7 or newer.

```console
pip install aioruuvigateway
```

## Usage

Ensure you have set up bearer token authentication in your Ruuvi Gateway (and that you know the token).

### API

Documentation can be found in `test_library.py` for now, sorry.

### Command line interface

You can use the command line interface to test the library.

```console
python -m aioruuvigateway --host 192.168.1.249 --token bearbear --parse --json
```

will output data from the gateway in JSON format, printing changed information every 10 seconds.

## License

`aioruuvigateway` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
