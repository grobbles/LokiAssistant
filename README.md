# Loki Assistant

![Build](https://github.com/grobbles/LokiAssistant/actions/workflows/release.yml/badge.svg)
[![PyPi version](https://badgen.net/pypi/v/loki-assistant/)](https://pypi.com/project/loki-assistant/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pybadges.svg)](https://pypi.python.org/pypi/loki-assistant/)
[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/loki-assistant/)

The Loki Assistant has been created to send log messages to the LOKI server. The labels can be specified individually.

# Install

You can install this package with pip tool from https://pypi.org/.

````bash
pip install loki-assistant
````

# Usage

There are three ways to send messages to the server.

## Each message individually

Sending every single message takes a lot of time. 6000 messages takes 3.67 s to send.

````python
from datetime import datetime
from loki_assistant import LokiAssistant

loki = LokiAssistant('http://localhost:3100/loki/api/v1/push', primary_tags={"application": "test"})

loki.post(loki.LogLevels.VERBOSE, {"thread": "1"}, datetime.now(), f"messsage: DEBUG")
loki.post(loki.LogLevels.DEBUG, {"thread": "1"}, datetime.now(), f"message: DEBUG")
loki.post(loki.LogLevels.INFO, {"thread": "1"}, datetime.now(), f"message: INFO")
loki.post(loki.LogLevels.WARNING, {"thread": "1"}, datetime.now(), f"message: WARNING")
loki.post(loki.LogLevels.ERROR, {"thread": "1"}, datetime.now(), f"message: ERROR")
loki.post(loki.LogLevels.FATAL, {"thread": "1"}, datetime.now(), f"message: FATAL")
````

## Collect messages

If several messages are sent together, a lot of time can be saved and the performance can be increased. Sending 60000 messages takes 0.660 s.

### Push all together

````python
from datetime import datetime
from loki_assistant import LokiAssistant

loki = LokiAssistant('http://localhost:3100/loki/api/v1/push', primary_tags={"application": "test"})

loki.commit(loki.LogLevels.VERBOSE, {"thread": "1"}, datetime.now(), f"messsage: DEBUG")
loki.commit(loki.LogLevels.DEBUG, {"thread": "1"}, datetime.now(), f"message: DEBUG")
loki.commit(loki.LogLevels.INFO, {"thread": "1"}, datetime.now(), f"message: INFO")
loki.commit(loki.LogLevels.WARNING, {"thread": "1"}, datetime.now(), f"message: WARNING")
loki.commit(loki.LogLevels.ERROR, {"thread": "1"}, datetime.now(), f"message: ERROR")
loki.commit(loki.LogLevels.FATAL, {"thread": "1"}, datetime.now(), f"message: FATAL")

loki.push()
````

### Push them over a time interval.

````python
from datetime import datetime
from loki_assistant import LokiAssistant

loki = LokiAssistant('http://localhost:3100/loki/api/v1/push', primary_tags={"application": "test"}, push_interval=1)

loki.commit(loki.LogLevels.VERBOSE, {"thread": "1"}, datetime.now(), f"messsage: DEBUG")
loki.commit(loki.LogLevels.DEBUG, {"thread": "1"}, datetime.now(), f"message: DEBUG")
loki.commit(loki.LogLevels.INFO, {"thread": "1"}, datetime.now(), f"message: INFO")
loki.commit(loki.LogLevels.WARNING, {"thread": "1"}, datetime.now(), f"message: WARNING")
loki.commit(loki.LogLevels.ERROR, {"thread": "1"}, datetime.now(), f"message: ERROR")
loki.commit(loki.LogLevels.FATAL, {"thread": "1"}, datetime.now(), f"message: FATAL")
````