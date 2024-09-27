import threading
import statistics
import time
import datetime
import random
import argparse
import csv

log_lock = threading.Lock()

def write_log(file, writer, tm, average, name, unit):
    with log_lock:
        print(f'[{tm.strftime('%d.%m.%Y %H:%M:%S')}] {name} = ~{average:.2f}{unit}')
        writer.writerow([tm, name, average, unit])
        file.flush()

def sensor_thread(args, logfile):
    data    = []
    fetches = 0
    logwriter = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    while True:
        fetches += 1
        data.append(random.uniform(args.min, args.max))
        if fetches >= args.interval:
            fetches = 0
            tm      = datetime.datetime.now()
            average = statistics.fmean(data)
            write_log(logfile, logwriter, tm, average, args.name, args.unit)
            data = []
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', default=60, type=int)
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--unit', type=str, required=True)
    parser.add_argument('--min', type=int, required=True)
    parser.add_argument('--max', type=int, required=True)
    args = parser.parse_args()

    with open('log.csv', 'a', newline='') as csvfile:
        t1 = threading.Thread(target=sensor_thread, args=(args,csvfile,))
        t2 = threading.Thread(target=sensor_thread, args=(args,csvfile,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
