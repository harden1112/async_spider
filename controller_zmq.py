import aiohttp
import asyncio
from datetime import datetime
import time
import zmq
import aiozmq
import logging
import json
from aiohttp import web
import yaml

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}


class ControllerDriver:
    def __init__(self, pull_port, push_port, reply_port, request_port):
        logging.info(
            "ControllerDriver portlist: pull:{}, push:{}, reply:{}, request:{}".format(pull_port, push_port, reply_port,
                                                                                       request_port))
        self._pull_port = pull_port
        self._push_port = push_port
        self._reply_port = reply_port
        self._request_port = request_port
        self._queue = asyncio.Queue()
        self._check_queue = asyncio.Queue()
        self._sql_queue = asyncio.Queue()
        self._async_check_queue = asyncio.Queue()
        self._async_queue = asyncio.Queue()
        self.game_list = []


    async def init(self, loop):
        app = web.Application(loop=loop)
        app.router.add_route('POST', "/score", self.score)
        srv = await loop.create_server(app.make_handler(), '0.0.0.0', 11675)
        print('Server started at http://47.90.0.38:11675...')
        return srv


    async def run_sql_check(self):
        self._sql_request = await aiozmq.create_zmq_stream(zmq.REQ, bind='tcp://127.0.0.1:8003')
        while True:
            data = await self._check_queue.get()
            data = json.dumps(data)
            data = [data.encode()]
            #print(data)
            data.append(b'1')
            #print(data, type(data))
            # request_msg = self.handle_request(data)
            self._sql_request.write(data)
            print("write")
            reply_msg = await self._sql_request.read()
            #print(reply_msg)
            self._sql_queue.put_nowait(reply_msg)
            #print(reply_msg)


    async def score(self, request):
        info = await request.text()
        info = json.loads(info)
        for i in info['app_ids']:
            request = {}
            request['category'] = 'steam_score'
            request['game_id'] = i
            request['steam_id'] = 'none'
            await self._queue.put(request)
        text = json.dumps({"data": "index"})
        return web.Response(body=text)



    async def run_loop(self):
        self._pull = await aiozmq.create_zmq_stream(zmq.PULL, bind='tcp://127.0.0.1:5555')
        self._push = await aiozmq.create_zmq_stream(zmq.PUSH, bind='tcp://127.0.0.1:5556')
        # self._push = await aiozmq.create_zmq_connection(zmq.PUSH, bind='tcp://*:{}'.format(self._push_port))
        while True:
            data = await self._pull.read()
            #print(data)
            self._push.write(data)
            print("send")

    async def run_reply(self):
        self._reply = await aiozmq.create_zmq_stream(zmq.PULL, bind='tcp://127.0.0.1:5559')
        while True:
            reply_msg = await self._reply.read()
            if reply_msg == [b'what']:
                print("whaaaaaaat")
            else:
                for i in reply_msg:
                    if len(i) >10:
                        print(i)
                        try:
                            page_json = json.loads(i.decode())
                            print(page_json)
                            json_list = {}
                            json_list["category"] = "comment_page"
                            json_list["steam_id"] =page_json['steam_id']
                            json_list["page"] = page_json['page']
                            print(json_list)
                            await self._queue.put(json_list)
                            #print('up'*6)
                        except:
                            pass
                        continue
                    json_list = {}
                    json_list["category"] = "game"
                    json_list["steam_id"] = reply_msg[0].decode()
                    json_list["game_id"] = i
                    await self._queue.put(json_list)
                    #print(json_list)
                print("finish push")
            #print("-"*890)

    async def run_request(self):
        import time
        self._request = await aiozmq.create_zmq_stream(zmq.REQ, bind='tcp://*:{}'.format(self._request_port))
        with open("input.yaml", "a") as ay:
            while True:
                print("started")
                try:
                    msg = await self._queue.get()
                    print(msg,type(msg))
                    input_data ={}
                    input_data['category_1'] = msg['category']
                    if msg['category'] == 'steam_score':
                        print(msg)
                        input_de_data ={}
                        input_de_data['category'] = msg['category']
                        input_de_data['time'] =time.strftime('%Y%m%d', time.localtime())
                        yaml.dump(input_de_data,ay)
                        msg_steam_id = str(msg['game_id'])
                        msg_steam_id = [msg_steam_id.encode()]
                        category = msg["category"].encode()
                        msg_steam_id.append(category)
                    else:
                        msg_steam_id = str(msg["steam_id"])
                        msg_steam_id = [msg_steam_id.encode()]
                        category = msg["category"].encode()
                        msg_steam_id.append(category)
                        if "game_id" in msg.keys():
                            game_id = msg['game_id']
                            msg_steam_id.append(game_id)
                        else:
                            pass
                except Exception as e:
                    print(e)
                    msg_steam_id = [b'finish']
                self._request.write(msg_steam_id)
                print("send")
                await self._request.drain()
                answer = await self._request.read()
                print(answer)
                # self._request.close()

    def handle_request(self):
        pass

    async def finish_check(self):
        while True:
            await  asyncio.sleep(1)
            msg = b'finish'
            return msg

    def handle_reply(self, reply_msg):
        print(reply_msg)

    async def send_request(self, msg):
        msg_dict = {}
        msg_dict["category"]='steam_score'
        msg_dict["game_id"] = msg
        await self._queue.put(msg_dict)


    def create_tasks(self):
        self._tasks = []
        self._tasks.append(asyncio.ensure_future(self.run_reply()))
        self._tasks.append(asyncio.ensure_future(self.run_request()))
        self._tasks.append(asyncio.ensure_future(self.run_loop()))
        return self._tasks

