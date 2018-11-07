import psutil
import json

cpu_p = psutil.cpu_percent(interval=0.1, percpu=True)
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

print(json.dumps(sys_param))
