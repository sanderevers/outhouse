import logging
import asyncio

__version__='0.1.0'

class DependencyProvider(dict):
    def __init__(self):
        super().__init__()
        self.registered = {}
        self.managers = []

    def register(self,cls,manager_factory,*args):
        self.registered[cls]=manager_factory,*args

    def __getitem__(self,cls):
        if cls in self:
            return super().__getitem__(cls)
        manager_factory,*args = self.registered[cls]
        log.debug('init {}'.format(cls))
        manager = manager_factory(*args)
        self.managers.append((cls,manager))
        try:
            inst = asyncio.create_task(manager.__aenter__())
        except AttributeError:
            try:
                inst = manager.__enter__()
            except AttributeError:
                inst = manager
        self[cls]=inst
        return super().__getitem__(cls)

    async def aget(self,cls):
        inst = self[cls]
        if hasattr(inst,'__await__'):
            return await inst
        else:
            return inst

    async def async_teardown(self):
        for cls,manager in self.managers:
            try:
                await manager.__aexit__(None,None,None)
                log.debug('async teardown {} completed'.format(cls))
            except AttributeError:
                try:
                    manager.__exit__(None,None,None)
                    log.debug('teardown {} completed'.format(cls))
                except:
                    pass
        self.managers = []

    def teardown(self):
        for cls,manager in self.managers:
            log.debug('teardown {}'.format(cls))
            try:
                manager.__exit__(None,None,None)
            except AttributeError:
                pass
        self.managers=[]

log = logging.getLogger(__name__)
