from json import loads
from time import sleep
from django.db import OperationalError
from kafka import KafkaConsumer
import sqlite3
from calculate.models import Calculation
from django.conf import settings
import cloudSEK.settings as app_settings
import django
settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS, DATABASES=app_settings.DATABASES)

django.setup()


consumer = KafkaConsumer(
    'calculation',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))


def consume():
    for message in consumer:
        data = message.value
        answer = data['number_1'] + data['number_2']
        c = Calculation.objects.get(pk=data['unique_identifier'])
        # try:
        #     with sqlite3.connect("../db.sqlite3", timeout=10) as conn:
        #         cursor = conn.cursor()
        #         query = f"UPDATE calculate_calculation SET answer = {answer} WHERE unique_identifier='{data['unique_identifier']}'"
        #         cursor.execute(query)
        #         conn.close()

        print(c, answer)
        sleep(10)

if __name__ == '__main__':
    consume()
