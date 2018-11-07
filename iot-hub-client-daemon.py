from iothub_client import IoTHubClient, IoTHubTransportProvider, IoTHubMessage
from daemonize import Daemonize
import psutil
import json
import time
import configparser
import logging

#Configuration
config = configparser.ConfigParser()
config.read('config.ini')

DAEMON_NAME = 'iot-hub-client'
CONNECTION_STRING = "HostName={};DeviceId={};SharedAccessKey={}".format(
        config.get('REMOTE','HostName'),
        config.get('REMOTE','DeviceId'),
        config.get('REMOTE','SharedAccessKey')
    )
PROTOCOL = IoTHubTransportProvider.MQTT
CPUDELAYSAMPLE = int(config.get('SAMPLE','CpuDelaySample'))
GLOBALDELAYSAMPLE = int(config.get('SAMPLE','GlobalDelaySample'))

#Daemon setup
pid = "/tmp/{}.pid".format(DAEMON_NAME)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler("/var/log/{}.log".format(DAEMON_NAME), "w")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

#Data gathering
def get_sys_params(sample_delay):
    cpu_p = psutil.cpu_percent(interval=sample_delay, percpu=True)
    cpu_t = psutil.sensors_temperatures()['cpu-thermal'][0][1]
    mem_p = psutil.virtual_memory()[2]
    dsk_p = psutil.disk_usage('/')[3]
    dsk_r = psutil.disk_io_counters(perdisk=False)[2]
    dsk_w = psutil.disk_io_counters(perdisk=False)[3]
    try:
        eth_i = psutil.net_io_counters(pernic=True)['eth0'][1]
        eth_o = psutil.net_io_counters(pernic=True)['eth0'][0]
    except:
        eth_i = 0
        eth_o = 0

    try:
        wln_i = psutil.net_io_counters(pernic=True)['wlan0'][1]
        wln_o = psutil.net_io_counters(pernic=True)['wlan0'][0]
    except:
        wln_i = 0
        wln_o = 0

    sys_param = {
        'cpu_0_p':cpu_p[0],
        'cpu_1_p':cpu_p[1],
        'cpu_2_p':cpu_p[2],
        'cpu_3_p':cpu_p[3],
        'cpu_t':cpu_t,
        'mem_p':mem_p,
        'dsk_p':dsk_p,
        'dsk_r':dsk_r,
        'dsk_w':dsk_w,
        'eth_i':eth_i,
        'eth_o':eth_o,
        'wln_i':wln_i,
        'wln_o':wln_o
    }

    return(sys_param)

def send_confirmation_callback(message, result, user_context):
    logger.debug("Conf ({})".format(result))

def main():
    while True:
        client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
        payload = json.dumps(get_sys_params(CPUDELAYSAMPLE))
        message = IoTHubMessage(payload)
        client.send_event_async(message, send_confirmation_callback, None)
        logger.debug("Msg sent")
        time.sleep(GLOBALDELAYSAMPLE)


if __name__ == '__main__':
    logger.debug("{} started".format(DAEMON_NAME))
    daemon = Daemonize(app=DAEMON_NAME, pid=pid, action=main, keep_fds=keep_fds)
    daemon.start()
