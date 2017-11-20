import asyncio
import aiohttp
from aiohttp import web
import async_timeout

async def handle_root(request):
    text = "Hello from python3.6+aiohttp"
    return web.Response(text=text)

async def handle_cpu_load(request):
    min_value = int(request.query.get('min', 1))
    max_value = int(request.query.get('max', 1000))
    s = sum(range(min_value, max_value + 1))
    text = "sum({}..{})={}".format(min_value, max_value, s)
    return web.Response(text=text)

async def handle_slow_resp(request):
    timeout = float(request.query.get('timeout', 1.0))
    await asyncio.sleep(timeout)
    text = "Slow hello from python3.6+aiohttp"
    return web.Response(text=text)

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def handle_gateway(request):
    url = request.query.get('url', 'http://localhost')
    session = request.app.client_session
    resp = await fetch(session, url)
    return web.Response(text=resp)

if __name__ == "__main__":
    app = web.Application()
    app.router.add_get('/', handle_root)
    app.router.add_get('/cpu_load', handle_cpu_load)
    app.router.add_get('/slow_resp', handle_slow_resp)

    app.client_session = aiohttp.ClientSession()
    app.router.add_get('/gateway', handle_gateway)

    web.run_app(app, port=3600)
