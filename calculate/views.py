from json import dumps, loads
from threading import Thread
from time import sleep

from django.http import HttpResponse
from calculate.models import Calculation
from kafka import KafkaProducer, KafkaConsumer
from settings import TOPIC_NAME

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

consumer = KafkaConsumer(
    'calculation',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

def home(request):
    return HttpResponse('Hi from test API', status=200)


def enter_numbers(request, number1, number2):
    cal = Calculation(number1=number1, number2=number2)
    data = {
        "number_1": number1,
        "number_2": number2,
        "unique_identifier": str(cal.get_unique_identifier())
    }
    producer.send(TOPIC_NAME, value=data)
    cal.save()

    return HttpResponse(f'{cal.get_unique_identifier()}')


def get_answer(request, identifier):
    try:
        cal = Calculation.objects.get(pk=identifier)
        answer = cal.get_answer()
        if answer:
            return HttpResponse(cal.get_answer(), status=200)
        else:
            return HttpResponse("please wait", status=200)
    except:
        return HttpResponse(status=404)


def consume():
    for message in consumer:
        data = message.value
        answer = data['number_1'] + data['number_2']
        try:
            c = Calculation.objects.get(pk=data['unique_identifier'])
            c.answer = answer
            c.save()
        except:
            pass
        sleep(10)

def start():
    consumer_t = Thread(target=consume, daemon=True)
    consumer_t.start()
    return

start()


