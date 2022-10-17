from django.shortcuts import render
import json

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from inventory.models import Product
from inventory.serializers import ProductSerializer


@api_view(['POST', 'GET'])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
        data = ProductSerializer(instance).data
        # serializer = ProductSerializer(data=request.data)

        # # Method #1
        # data['id'] = model_data.id
        # data['name'] = model_data.name
        # data['title'] = model_data.title
        # data['content'] = model_data.content
        # data['description'] = model_data.description

        # # Method #2
        # data = model_to_dict(instance, fields=['web_id',\
        #                                         'slug',\
        #                                         'name',\
        #                                         'title',\
        #                                         'content',\
        #                                         'description',\
        #                                         'public',\
        #                                         'price',\
        #                                         'is_active',\
        #                                         'body',\
        #                                         'sale_price',\
        #                                         'path',\
        #                                         'endpoint',\
        #                                         'get_absolute_url',\
        #                                         'is_public',\
        #                                         'get_tags_list',\
        #                                         'my_discount'\
        #                                         ])
        #
        # print(data)
        # data = request.data
        return Response(data)


    # if serializer.is_valid(raise_exception=True):
    # #     instance = serializer.save()
    # #     instance = form.save()
    # #     print(serializer.data)
    #     return Response(serializer.data)
    return Response({"invalid": "not good data"}, status=400)













def api_index(request, *args, **kwargs):
    data = {}

    return JsonResponse({'data':data, 'param':"test"})

def index(request, *args, **kwargs):
    response_data = {"message":"hi tthere response"}
    print(request.GET) # URL query params
    # print(request.POST) # URL query params
    body = request.body
    try:
        data = json.loads(body)
    except:
        data={}
    data['params'] = dict(request.GET) # not fson searliszable without
    data['header'] = dict(request.headers) # not fson searliszable without
    data['content_type'] = request.content_type
    print(data.keys())
    print(body)
    return JsonResponse({'response_data':response_data, 'data':data, 'param':"test"})

@api_view(['GET','POST'])
def product_home_raw(request, *args, **kwargs):
    # model_data  = {}
    instance  = Product.objects.all().order_by('?').first()

    data = {}

    if instance:
        data = ProductSerializer(instance).data
        # # Method #2
        # data = model_to_dict(instance, fields=['id', 'name', 'title', 'content', 'description'])
        # # Method #1
        # data['id'] = model_data.id
        # data['name'] = model_data.name
        # data['title'] = model_data.title
        # data['content'] = model_data.content
        # data['description'] = model_data.description

    return Response({'data':data, 'param':"test"})

def server_info(request):
    response_data = {}

    import netifaces as ni
    # ni.ifaddresses('eth0')
    # _ip = _ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    # print(ip)  # should print "192.168.100.37"
    # You can also get a list of all available interfaces via

    # ni.interfaces()
    # response_data['INTERFACES'] = ni.interfaces()
    # _interface_list = response_data['INTERFACES']

    _addr_families = [ni.AF_LINK, ni.AF_INET, ni.AF_INET6 ]
    _interface_list = ni.interfaces()
    response_data['INTERFACES'] = {}

    for _idx, _interface in enumerate(_interface_list):
        response_data['INTERFACES'][_interface] = {'UNPACK': ni.ifaddresses(_interface)}
        response_data['INTERFACES'][_interface] = {}

        for _family in _addr_families:
            # try:
            #     response_data['INTERFACES'][_interface]['LINK_ADDR'] = ni.ifaddresses(_interface)[ni.AF_LINK][0]['addr']
            # except:
            #     pass

            try:
                response_data['INTERFACES'][_interface]['IP'] = ni.ifaddresses(_interface)[ni.AF_INET][0]['addr']
            except:
                pass

            # try:
            #     response_data['INTERFACES'][_interface]['IPV6'] = ni.ifaddresses(_interface)[ni.AF_INET6][0]['addr']
            # except:
            #     pass

    response_data['TEMP'] = 99.0
    response_data['HUMIDITY'] = 99.0
    response_data['CPU_TEMP'] = 99.0
