import time
from datetime import datetime

from plyty.order_csv_exporter import export_orders, export_total_user_orders
from plyty.scheduler_config import GENERATION_REPORT_INTERVAL_SECONDS, GENERATION_REPORT_START_MINUTE, \
    GENERATION_REPORT_START_HOUR


def export_orders_task():
    print("\nJob generowania raportów zamówień zarejestrowany\n")
    while True:
        now = datetime.now()
        if now.hour == GENERATION_REPORT_START_HOUR and now.minute == GENERATION_REPORT_START_MINUTE:
            print("Generowanie raportu zamówień: ", datetime.now().strftime("%m_%d_%Y__%H:%M:%S"))
            export_orders()
            print("Generowanie raportu ilości zamówień użytkowników: ", datetime.now().strftime("%m_%d_%Y__%H:%M:%S"))
            export_total_user_orders()
            time.sleep(GENERATION_REPORT_INTERVAL_SECONDS)
        else:
            time.sleep(10)  # check every 10 seconds
