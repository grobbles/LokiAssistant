import logging
import uuid
from datetime import datetime
from unittest import TestCase

from loki_assistant import LokiAssistant

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-10.10s | %(name)-30.30s | %(message)s")
log = logging.getLogger()


class TestPySignal(TestCase):

    def test_post_message(self):
        run_id = str(uuid.uuid4())
        loki = LokiAssistant('http://localhost:3100/loki/api/v1/push', primary_tags={"application": "test", "id": run_id})
        for i in range(100):
            loki.post(LokiAssistant.LogLevels.VERBOSE, {"pid": "1", "thread": "1"}, datetime.now(), f"message: {i}")
            loki.post(LokiAssistant.LogLevels.DEBUG, {"thread": "1"}, datetime.now(), f"message: {i}")
            loki.post(LokiAssistant.LogLevels.INFO, {"thread": "1"}, datetime.now(), f"message: {i}")
            loki.post(LokiAssistant.LogLevels.WARNING, {"thread": "1"}, datetime.now(), f"message: {i}")
            loki.post(LokiAssistant.LogLevels.ERROR, {"thread": "1"}, datetime.now(), f"message: {i}")
            loki.post(LokiAssistant.LogLevels.FATAL, {"thread": "1"}, datetime.now(), f"message: {i}")

    def test_commit_massages_and_post_all(self):
        run_id = str(uuid.uuid4())
        loki = LokiAssistant('http://localhost:3100/loki/api/v1/push', primary_tags={"application": "test", "id": run_id})
        for i in range(10000):
            loki.commit(loki.LogLevels.VERBOSE, {"pid": "1", "thread": "1"}, datetime.now(), f"messsage: {i}")
            loki.commit(loki.LogLevels.DEBUG, {"thread": "1"}, datetime.now(), f"messagess: {i}")
            loki.commit(loki.LogLevels.INFO, {"thread": "1"}, datetime.now(), f"messagess: {i}")
            loki.commit(loki.LogLevels.WARNING, {"thread": "1"}, datetime.now(), f"messssage: {i}")
            loki.commit(loki.LogLevels.ERROR, {"thread": "1"}, datetime.now(), f"messsage: {i}")
            loki.commit(loki.LogLevels.FATAL, {"thread": "1"}, datetime.now(), f"messsage: {i}")
        loki.push()

    def test_commit_massages_and_post_over_thread(self):
        run_id = str(uuid.uuid4())
        loki = LokiAssistant('http://localhost:3100/loki/api/v1/push', primary_tags={"application": "test", "id": run_id}, push_interval=2)
        for i in range(10000):
            loki.commit(loki.LogLevels.VERBOSE, {"pid": "1", "thread": "1"}, datetime.now(), f"messsage: {i}")
            loki.commit(loki.LogLevels.DEBUG, {"thread": "1"}, datetime.now(), f"messagess: {i}")
            loki.commit(loki.LogLevels.INFO, {"thread": "1"}, datetime.now(), f"messagess: {i}")
            loki.commit(loki.LogLevels.WARNING, {"thread": "1"}, datetime.now(), f"messssage: {i}")
            loki.commit(loki.LogLevels.ERROR, {"thread": "1"}, datetime.now(), f"messsage: {i}")
            loki.commit(loki.LogLevels.FATAL, {"thread": "1"}, datetime.now(), f"messsage: {i}")
