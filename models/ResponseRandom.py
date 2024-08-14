from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Random:
    data: List[str]
    completionTime: str

    @staticmethod
    def from_dict(obj: Any) -> 'Random':
        _data = [y for y in obj.get("data")]
        _completionTime = str(obj.get("completionTime"))
        return Random(_data, _completionTime)

@dataclass
class Result:
    random: Random
    bitsUsed: int
    bitsLeft: int
    requestsLeft: int
    advisoryDelay: int

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        _random = Random.from_dict(obj.get("random"))
        _bitsUsed = int(obj.get("bitsUsed"))
        _bitsLeft = int(obj.get("bitsLeft"))
        _requestsLeft = int(obj.get("requestsLeft"))
        _advisoryDelay = int(obj.get("advisoryDelay"))
        return Result(_random, _bitsUsed, _bitsLeft, _requestsLeft, _advisoryDelay)

@dataclass
class ResponseRandom:
    jsonrpc: str
    result: Result
    id: int

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _jsonrpc = str(obj.get("jsonrpc"))
        _result = Result.from_dict(obj.get("result"))
        _id = int(obj.get("id"))
        return ResponseRandom(_jsonrpc, _result, _id)

 