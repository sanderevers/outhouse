# outhouse

_Because who wants indoor plumbing?_

`outhouse` is a no-nonsense dependency injection provider for Python
applications. In particular, it supports async initialization.

## Install
```
pip install outhouse
```

## Usage

Let's say you want to inject `aiohttp`'s
[ClientSession](https://docs.aiohttp.org/en/stable/client_reference.html)
connection pool into your application. First, tell the framework how to
setup and tear down a `ClientSession` instance, using the (async) context
manager protocol:

```python
from contextlib import asynccontextmanager
from aiohttp import ClientSession

@asynccontextmanager
async def manage_clientsession():
    session = ClientSession()
    yield session
    await session.close()
```

Then, register this at the dependency provider. The place to keep a
global dependency provider is in the app's global state. For `aiohttp`,
it works like this:

```python
from outhouse import DependencyProvider

def create_app():
    d = DependencyProvider()
    d.register(aiohttp.ClientSession, manage_clientsession)
    app = aiohttp.web.Application()
    app['d'] = d
```

Next, use the `ClientSession` instance somewhere in your app:

```python
async def somewhere(app):
    session = await app['d'].aget(aiohttp.ClientSession)
    async with session.get('https://python.org') as resp:
        ...
```

