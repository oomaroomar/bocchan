from pyspectator.processor import Cpu
from datetime import datetime
import os
import time
import pandas as pd
import matplotlib.pyplot as plt


def current_milli_time(): return int(time.time()*1000)


cpu = Cpu(monitoring_latency=1)
monkaS_temp = 60


def temp_monitor(length=128, interval=1.1) -> list:
    temps = []
    until = current_milli_time() + length * 1000
    with cpu:
        while(current_milli_time() < until):
            temps.append((datetime.now().strftime('%T'), cpu.temperature))
            time.sleep(interval)

    return temps


def get_tempgraph_path():
    # Helper variables
    today = datetime.now().strftime('%d.%m.%Y')
    path = os.path.dirname(os.path.abspath(__file__))

    # Get the juice
    output = temp_monitor()
    temps = pd.DataFrame(output)
    temps.columns = ['timestamp', 'temperature']
    worrysome = temps['temperature'].max() >= monkaS_temp

    ticks = get_ticks(len(temps), i=int(len(temps)/8))  # i = n / 2t
    log_path = f'{path}/logs/{today}_{temps["timestamp"][0]}.jpg'

    # Drawing
    plt.ylim(20, 100), plt.title(today), plt.xticks(ticks)
    plt.ylabel('°C', rotation=0, fontsize=14, labelpad=18)
    plt.plot(temps['timestamp'], temps['temperature'])
    plt.savefig(log_path,
                format='jpg', pil_kwargs={'quality': 85})
    plt.close()

    return log_path, worrysome


def get_ticks(n: int, l=0.0, i=1, t=4) -> list:
    if i > n:  # base case
        return []
    if l >= 1:
        return [i] + get_ticks(n, l-1, int(i + 1 + n/t))
    else:
        return [i] + get_ticks(n, l + n % t, int(i + n/t))
