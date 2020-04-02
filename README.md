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

users table:

|   field   |   type    | description |
| ----      | -------   | -------     |
| id        | uint32    | auto increment key id |
| steam_user_id  | uint64    | steam id |

games table:

|   field   |   type    | description |
| ----      | -------   | -------     |
| id        | uint32    | auto increment key id |
| steam_game_id   | varchar(64)| steam game id |

achievements table:

|   field   |   type    | description |
| ----      | -------   | -------     |
| id        | uint32    | auto increment key id |
| achievement | varchar(64)| steam game id of achievement |
| description | varchar(128) | description of the achievement |
| unlock_time | timestamp | unlock time stamp |
| game_id | uint32 | id of the belonged game |
| user_id | uint32 | id of the belonged user |

friends table:

|   field   |   type    | description |
| ----      | -------   | -------     |
| id        | uint32    | auto increment key id |
| user_id   | uint32    | user id in user table |
| steam_friend_id | uint64    | steam id of the friend |
