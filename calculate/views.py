from json import dumps
from django.http import HttpResponse
from calculate.models import Calculation
from kafka import KafkaProducer
from settings import TOPIC_NAME

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))


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
    print(data)
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
    except :
        return HttpResponse(status=404)



