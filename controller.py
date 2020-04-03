import logging
from controller_zmq import ControllerDriver
import asyncio
from aioconsole import ainput


class ControllerServer:
    def __init__(self):
        pass

    def create_tasks(self, controller):
        return asyncio.ensure_future(self.start(controller))

    async def start(self, controller):
        while True:
            """Id setup"""
            user = await ainput(prompt="please input steam id >")
            if user == '8888':
                loop = asyncio.get_event_loop()
                loop.stop()
                break
            await controller.fetch_user(user)


class Controller:
    def __init__(self, driver, server):
        self._driver = driver
        self._server = server
        self._tasks = []

    async def process(self):
        while True:
            await asyncio.sleep(1)
            # pass

    def start_driver(self):
        self._tasks.append(self._driver.create_tasks())

    def start_server(self):
        self._tasks.append(self._server.create_tasks(self))

    async def fetch_user(self, user):
        await self._driver.send_request(user)


class ControllerRunner:
    def __init__(self, params):
        self._pull_addr = params['controller']['pull']['addr']
        self._pull_port = params['controller']['pull']['port']
        self._push_addr = params['controller']['push']['addr']
        self._push_port = params['controller']['push']['port']
        self._reply_addr = params['controller']['reply']['addr']
        self._reply_port = params['controller']['reply']['port']
        self._request_addr = params['controller']['request']['addr']
        self._request_port = params['controller']['request']['port']

    def run(self):
        pass

    def test_run(self):
        driver = ControllerDriver(self._pull_port,
                                  self._push_port,
                                  self._reply_port,
                                  self._request_port)
        server = ControllerServer()
        controller = Controller(driver, server)
        controller.start_driver()
        controller.start_server()
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(controller.process())
        """Server setup"""
        # loop.run_until_complete(driver.init(loop))
        loop.run_forever()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import argparse
    import yaml
    parser = argparse.ArgumentParser(description='The controller service')
    parser.add_argument('-c', '--conf', metavar='config file', dest='conf', default='conf.yaml',
                        help='the configuration file')
    args = parser.parse_args()
    with open(args.conf) as cf:
        params = yaml.load(cf)
    runner = ControllerRunner(params)
    runner.test_run()

