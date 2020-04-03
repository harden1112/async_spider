# crawler system

## design

To simplify the whole system and to implement the high expansion goals, the 
spider system will divide into several parts as the following:

![architecture](./doc/architecture.png)

We'll go through all the services in the graph in brief.

The fetcher service is the one to fetch data from the specific website 
through the proxy server.

The parser service take the charge of parsing the fetched data and extract
the information we need.

The storage service will help other parts to store the required information into
the database service for persistent storage.

The control service was the interfaces of the whole system.

## implementation

### data flow


### technology

1. ZeroMQ:
2. Python3:
3. asyncio:
4. aiomysql:
5. aiohttp:
6. aiozmq:

### service topology

#### control service

#### fetcher service

#### parser service

#### storage service


games table:

|   field   |   type    | description |
| ----      | -------   | -------     |
| id        | uint32    | auto increment key id |
| app_id    | varchar(32)| game id  |
| review    | varchar(32)| game score  |
| number    | varchar(32)| game numbers|
| per_cent  | varchar(32)| per cent |

