import time
from datetime import datetime

from plyty.order_csv_exporter import export_orders


def export_orders_task():
    print("\nJob generowania raportów zamówień zarejestrowany\n")
    while True:
        now = datetime.now()
        if now.hour == 20 and now.minute == 43:
            print("Generowanie raportu zamówień: ", datetime.now().strftime("%m_%d_%Y__%H:%M:%S"))
            export_orders()
            time.sleep(24 * 60 * 60 - 120)  # sleep almost 24h
        else:
            time.sleep(10)  # check every 10 seconds
