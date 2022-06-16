import copy
import json
import logging
import threading
import time
from datetime import datetime
from enum import Enum
from typing import Optional, Tuple, Dict, List

import requests

BasicAuth = Optional[Tuple[str, str]]


class LokiAssistant:
    class LogLevels(Enum):
        VERBOSE = "VERBOSE"
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        FATAL = "FATAL"

    LEVEL_TAG: str = "level"

    def __init__(self, url: str, auth: BasicAuth = None, primary_tags: Dict[str, str] = None, push_interval: int = 0):
        self._log = logging.getLogger()

        self._url = url
        self._auth = auth
        self._session: Optional[requests.Session] = None
        self._primary_tags = primary_tags
        self._push_interval = push_interval

        self._message_cache_lock = threading.Lock()
        self._message_cache = {}

        if self._push_interval > 0:
            self._push_thread = threading.Thread(target=self._push_runner)
            self._push_thread.start()
        pass

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session
            self._session.auth = self._auth or None
        return self._session

    def close(self):
        if self._session is not None:
            self._session.close()
            self._session = None

    def commit(self, log_level: LogLevels, log_labels: Dict[str, str], timestamp: datetime, message: str):
        log_labels[self.LEVEL_TAG] = log_level.value.lower()

        key = json.dumps(log_labels)

        self._message_cache_lock.acquire()
        if key not in self._message_cache:
            self._message_cache[key] = []
        self._message_cache[key].append(self._create_message(timestamp, message))
        self._message_cache_lock.release()
        pass

    def _push_runner(self):
        while True:
            try:
                if len(self._message_cache) > 0:
                    self.push()
                time.sleep(self._push_interval)
            except Exception as e:
                self._log.warning(f"catch exception: {e}")
        pass

    def push(self):
        self._message_cache_lock.acquire()
        message_cache = copy.deepcopy(self._message_cache)
        self._message_cache = {}
        self._message_cache_lock.release()

        streams = []
        for labels, values in message_cache.items():
            stream = {
                "stream": {**self._primary_tags, **json.loads(labels)},
                "values": values
            }
            streams.append(stream)

        message = {
            "streams": streams
        }
        self._emit(message)
        pass

    def post(self, log_level: LogLevels, log_labels: Dict[str, str], timestamp: datetime, message: str):
        log_labels[self.LEVEL_TAG] = log_level.value.lower()

        message = {
            "streams": [
                {
                    "stream": {**self._primary_tags, **log_labels},
                    "values": [self._create_message(timestamp, message)]
                }
            ]
        }
        self._emit(message)
        pass

    @classmethod
    def _create_message(cls, timestamp: datetime, message: str) -> List[str]:
        timestamp_ns = int(timestamp.timestamp() * 1000 * 1000 * 1000)
        return [str(timestamp_ns), message]

    def _emit(self, message):
        resp = requests.post(self._url, json=message)
        if resp.status_code != 204:
            raise ValueError(f"Unexpected Loki API response status code: {resp.status_code}")
        pass
