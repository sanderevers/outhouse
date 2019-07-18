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
    app.on_shutdown.append(teardown_deps)
    return app

async def teardown_deps(app):
    await app['d'].async_teardown()
```

Next, use the `ClientSession` instance somewhere in your app:

```python
async def somewhere(app):
    session = await app['d'].aget(aiohttp.ClientSession)
    async with session.get('https://python.org') as resp:
        ...
```

The first call to `aget` will setup the `ClientSession` instance.
Subsequent calls will return the same instance.

An often occurring pattern is injecting dependencies into dependencies:

```python
class TwitterClient:
    def __init__(self,config,session):
        self.config = config
        self.session = session

    async def setup_access_token(self):
        url = self.config.TWITTER_TOKEN_URL
        async with self.session.post(url, ...) as resp:
            ...

    @staticmethod
    @asynccontextmanager
    async def manage_me(d):
        client = TwitterClient(d['config'], await d.aget(aiohttp.ClientSession))
        await client.setup_access_token()
        yield client
```
At the app configuration, pass the dependency provider:
```python
d.register(TwitterClient,TwitterClient.manage_me,d)
```
Registering simple dependencies is possible without a context manager.
```python
d.register('config',lambda: read_config_file())

```