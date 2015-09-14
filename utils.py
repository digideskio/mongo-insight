from itertools import zip_longest
import logging
from requests.exceptions import RequestException
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import SSLError


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def get_nested_items(obj, *names):
    """Return obj[name][name2] ... [nameN] for any list of names."""
    for name in names:
        obj = obj[name]
    return obj


def configure_logging(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def write_points(logger, client, json_points, line_number):
    # TODO - I originally wrote this to reduce code duplication - however, we need a better way to handle all the parameters
    try:
        client.write_points(json_points)
        logger.info("Wrote in {} points to InfluxDB. Processed up to line {}.".format(len(json_points), line_number))
    except RequestException as e:
        logger.error("Unable to connect to InfluxDB at {} - {}".format(client._host, e))
    except InfluxDBClientError as e:
        logger.error('Unable to write to InfluxDB - {}'.format(e))
    except SSLError as e:
        logger.error('SSL error - {}'.format(e))