#!/usr/bin/env python
import logging
import asyncio
import configparser

from aiocoap import *

def read_config(config_ini):
    config = configparser.ConfigParser()
    config.read(config_ini)

    try:
        if config.has_section("Client"):
            host = config["Client"]["host"]
        else:
            print("No client config found with Client section")
    except KeyError as e:
        print("Host key not found in client config")
        

    return host

logging.basicConfig(level=logging.INFO)

async def main():
    client = await Context.create_client_context()

    host = read_config(config_ini="client_config.ini")
    uri = 'coap://' + host + '/temp'

    request = Message(code=GET, uri=uri)

    try:
        response = await client.request(request).response
    except Exception as e:
        print("Failed to fetch resource:")
        print(e)
    else:
        print("Server response: %s " %(response.payload.decode("utf-8")))

if __name__ == "__main__":
    asyncio.run(main())