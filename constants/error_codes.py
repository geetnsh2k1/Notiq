from enum import Enum


class ErrorCodes:
    class Client(int, Enum):
        CREATE_FAILED = 2001
        GET_BY_ID_FAILED = 2002
        GET_BY_API_KEY_FAILED = 2003
        NOT_FOUND = 2004
        UPDATE_STATUS_FAILED = 2005
        GET_ALL_FAILED = 2006
        DELETE_FAILED = 2007
        GET_BY_NAME_FAILED = 2008

    class Channel(int, Enum):
        CREATE_FAILED = 2101
        GET_BY_ID_FAILED = 2102
        GET_BY_NAME_FAILED = 2103
        UPDATE_STATUS_FAILED = 2104
        NOT_FOUND = 2105
        GET_ALL_FAILED = 2106
        DELETE_FAILED = 2107

    class Provider(int, Enum):
        CREATE_FAILED = 2201
        GET_BY_ID_FAILED = 2202
        GET_BY_CHANNEL_ID_FAILED = 2203
        UPDATE_STATUS_FAILED = 2204
        NOT_FOUND = 2205
        GET_ALL_FAILED = 2206
        DELETE_FAILED = 2207
    
    class Receiver(int, Enum):
        CREATE_FAILED = 2301
        GET_BY_ID_FAILED = 2302
        GET_BY_CLIENT_ID_FAILED = 2303
        DELETE_FAILED = 2304
        NOT_FOUND = 2305

    class Template(int, Enum):
        CREATE_FAILED = 2401
        GET_BY_ID_FAILED = 2402
        GET_ALL_FAILED = 2403
        GET_BY_PROVIDER_ID_FAILED = 2404
        GET_BY_CHANNEL_ID_FAILED = 2405
        DELETE_FAILED = 2406
        NOT_FOUND = 2407
        UPDATE_FAILED = 2408

    class Request(int, Enum):
        CREATE_FAILED = 2501
        GET_BY_ID_FAILED = 2502
        GET_BY_RECEIVER_FAILED = 2503
        STATUS_UPDATE_FAILED = 2504
