from django.http import HttpResponse
import logging
logger = logging.getLogger('django')
def index(request):
    a, b = 2, 0
    try:
        a / b
    except Exception as e:
        logger.exception(e)
    return HttpResponse("You have an excepion, see console and log")




















