import subprocess
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from datetime import datetime
import os

monkaS_temp = 60


def get_temperatures():
    today = datetime.now().strftime('%d.%m.%Y')
    path = os.path.dirname(os.path.abspath(__file__))
    output = StringIO(subprocess.getoutput(path + '/templogger.sh'))

    temps = pd.read_csv(output)
    temps.columns = ['timestamp', 'temperature']

    first_time = temps['timestamp'][0]
    log_path = f'{path}/logs/{today}_{first_time}.jpg'
    ticks = get_ticks(len(temps), i=int(len(temps)/8))  # i = n / 2t
    print(ticks)

    plt.ylim(20, 100)
    plt.plot(temps['timestamp'], temps['temperature'])
    plt.title(today)
    plt.ylabel('°C', rotation=0, fontsize=14, labelpad=18)
    plt.xticks(ticks)
    plt.savefig(log_path,
                format='jpg', pil_kwargs={'quality': 85})
    plt.close()

    worrysome = temps['temperature'].max() >= monkaS_temp

    return log_path, worrysome


def get_ticks(n: int, l=0.0, i=1, t=4) -> list:
    if i > n:  # base case
        return []
    if l >= 1:
        return [i] + get_ticks(n, l-1, int(i + 1 + n/t))
    else:
        return [i] + get_ticks(n, l + n % t, int(i + n/t))

