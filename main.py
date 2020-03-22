from aiohttp import web
from zigbee_controller import ZigbeeController
import asyncio
import os
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

web_app = web.Application()
routes = web.RouteTableDef()
zigbee_controller = ZigbeeController()


@routes.post('/permitjoin')
async def permit_join(request):
    LOGGER.info("permitting devices to joing for the next 60s ...")
    permit_join_future = asyncio.create_task(zigbee_controller.permit_join())
    permit_join_future.add_done_callback(lambda future: LOGGER.info("devices can no longer join the network"))
    return web.Response()


@routes.get('/devices')
async def devices(request):
    return web.json_response(zigbee_controller.get_devices())


@routes.post('/{device_ieee}')
async def control_device(request):
    device_ieee = int(request.match_info['device_ieee'])
    body = await request.json()

    if "params" not in body:
        body["params"] = ""

    try:
        await zigbee_controller.send_command(device_ieee, body["command"], body["params"])
    except Exception as e:
        LOGGER.exception("Failed to control device!")
        return web.Response(status=500, text=str(e))

    return web.Response()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(zigbee_controller.setup_network())

    web_app.add_routes(routes)
    web.run_app(web_app, port=os.getenv('PORT', 8080))
