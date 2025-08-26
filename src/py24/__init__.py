# Copyright 2025 Lordseriouspig
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

class Pi24NotFound(Exception):
    """Pi24 was not found on the host"""

class Pi24ConnectionError(Exception):
    """Could not connect to the host"""

class Pi24UnknownError(Exception):
    """An unknown error occurred"""

def get_monitor(ip,port=8754,filter=None):
    try:
        r = requests.get(f"http://{ip}:{port}/monitor.json")
        r.raise_for_status()
        if filter:
            return [item for item in r.json() if filter in item]
        else:
            return r.json()
    except requests.RequestException as e:
        raise Pi24ConnectionError(f"Could not connect to {ip}:{port} - {str(e)}")
    except Exception as e:
        raise Pi24UnknownError(f"An unknown error occurred: {str(e)}")

def get_flights(ip,port=8754):
    try:
        r = requests.get(f"http://{ip}:{port}/flights.json")
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise Pi24ConnectionError(f"Could not connect to {ip}:{port} - {str(e)}")
    except Exception as e:
        raise Pi24UnknownError(f"An unknown error occurred: {str(e)}")

def exists(ip,port=8754):
    try:
        r = requests.get(f"http://{ip}:{port}/monitor.json")
        r.raise_for_status()
        assert "feed_status" in r.json()
        return True
    except requests.RequestException as e:
        raise Pi24ConnectionError(f"Could not connect to {ip}:{port} - {str(e)}")
    except AssertionError:
        raise Pi24NotFound(f"An instance of Pi24 was not found or returned corrupted data on {ip}:{port}")
    except Exception as e:
        raise Pi24UnknownError(f"An unknown error occurred: {str(e)}")