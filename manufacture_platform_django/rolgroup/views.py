from urllib import response

import qrcode
import transitions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import *
import json
import traceback
import functools

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import datetime, timedelta
import pytz
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

from qrcode import make, QRCode
from qrcode.exceptions import DataOverflowError
import base64


from .cutting import cutting
#import importlib

#importlib.import_module(os.path.join(BASE_DIR, 'cutting'))

from . import serializers

from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from .models import userProfile
from .license import IsOwnerProfileOrReadOnly
from .permissions import *
from .serializers import userProfileSerializer

#редактирование данных
#@renderer_classes((JSONRenderer))


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        #print(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.username,
            'email': user.email
        })



def convert_to_UTC(local_tz, dt_1, dt_2):
    format='%Y-%m-%d'
    pytz_local_tz = pytz.timezone(local_tz)
    dt_obj_from_date_time = datetime.strptime(dt_1, format)
    dt_obj_to_date_time = datetime.strptime(dt_2, format)
    return [pytz_local_tz.localize(dt_obj_from_date_time).astimezone(tz=pytz.utc).strftime(format),
            pytz_local_tz.localize(dt_obj_to_date_time).astimezone(tz=pytz.utc).strftime(format)]


def ret(json_object, status=200):
    return JsonResponse(
        json_object,
        status=status
    )


def error_response(exception):
    res = {
        "error_message": str(exception),
        "traceback": traceback.format_exc()
    }
    return ret(res, 400)


def base_view(fn):
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            #with transitions.atomic():
            return fn(request, *args, **kwargs)
        except KeyError as e:
            #print(e)
            return error_response("KeyError" + str(e))
        except Exception as e:
            print(e)
            return error_response(e)
    return inner


class UserProfileListCreateView(ListCreateAPIView):
    queryset = userProfile.objects.all()
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = userProfile.objects.all()
    serializer_class = userProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]




# @csrf_exempt
def index(request):
    if request.method == 'POST':pass


class ColorsList(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ManagerAllEditOrReadOnly,)
    queryset = Colors.objects.all()
    serializer_class = serializers.ColorsSerializer


class ProjectList(viewsets.ModelViewSet):
    permission_classes = (ManagerAllEditOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class CompositiontList(viewsets.ModelViewSet):
    permission_classes = (ManagerAllEditOrReadOnly,)
    queryset = Composition.objects.all()
    serializer_class = serializers.CompositionSerializer


class StocktList(viewsets.ModelViewSet):
    permission_classes = (WorkerAllEditOrReadOnly,)
    queryset = Stock.objects.all()
    serializer_class = serializers.StockSerializer



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000




class ArticleView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Composition.objects.all()
    serializer_class = Composition
    def get(self, request, *args, **kwargs):
        return #self.list(request, *args, **kwargs)
    def perform_create(self, serializer):
        #author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        return #serializer.save(author=author)

    def post(self, request, *args, **kwargs):


        return #self.create(request, *args, **kwargs)


class SomethingAPIView(generics.ListAPIView):pass


@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def upload_file(request):
    data = request.data
    avatar = request.FILES.get('file')
    fs = FileSystemStorage()
    filename = fs.save(avatar.name, avatar)
    #data = json.loads(request.body)
    params = {
        'name': data["name"],
        'name_dow': data["name_dow"],
        'file': filename,
    }
    Documents.objects.create(**params)
    return JsonResponse({'status': 'ok'})


@api_view(['POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    #if request.method == 'POST':
    rollets = []
    compositions = []
    for i in request.data["data"]:
        rollets += Rollets.objects.filter(project_id=i)
    for i in rollets:
        compositions += Composition.objects.filter(rollets_id=i.id)


    
    serializer = serializers.CompositionSerializer(compositions, many=True)

    # if serializer.is_valid():pass
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    print("Hwllo")
    return Response(serializer.data)#, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@base_view
def project_rollets(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    # if request.method == 'POST':
    #rollets = []
    rollets = []
    for i in request.data["project_ids"]:
        rollets += Rollets.objects.filter(project_id=i)
    # for i in rollets:
    #     compositions += Composition.objects.filter(rollets_id=i.id)

    # serializer = serializers.RolletsSerializer(rollets, many=True)

    res = []

    for r in rollets:
        color = '-'
        if r.parts.color_id:
            color = r.parts.color_id.color_short
        res.append({
            "rollet_id": r.id,
            "width": r.width,
            "height": r.height,
            "project": r.project.id,
            "status_packed": r.status_packed,
            "material": str(r.parts.material_id),
            "color": color
        })

    # if serializer.is_valid():pass
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse({'status': 'ok', "results": res}, status=200)


@api_view(['POST'])
@base_view
def project_composition(request):

    project_id = request.data["project_id"]
    rollet_id = request.data["rollet_id"]

    compositions = []

    rollets = Rollets.objects.filter(id=rollet_id, project_id=project_id)

    for i in rollets:
        composition = Composition.objects.filter(rollets_id=i.id)
        ccc = []
        for c in composition:
            color = '-'
            if c.parts.color_id:
                color = c.parts.color_id.color_short
            # print(c.length, c.need_count, c.quantity, color, c.parts.material_id, c.parts.material_id.class_id)
            ccc.append({
                'length': c.length,
                'need_count': c.need_count,
                'quantity': c.quantity,
                'color': color,
                'material': str(c.parts.material_id),
                'class': str(c.parts.material_id.class_id)
            })
        compositions.append(ccc)


    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse({'status': 'ok', "results": compositions}, status=200)



@api_view(['POST'])
@base_view
def assemble_the_roller(request):

    project_id = request.data["project_id"]
    rollet_id = request.data["rollet_id"]
    rollets = Rollets.objects.filter(id=rollet_id, project_id=project_id)

    if not(rollets) or not(project_id) or not(rollet_id):
        return JsonResponse({'status': 'error', "text": "Неправильно выбрана роллета"}, status=200)
    
    composition = Composition.objects.filter(rollets_id=rollets[0].id)

    need_to_cut = []
    need_to_order = []

    for c in composition:
        if c.parts.material_id.class_id.dim.can_cut:
            if c.need_count == c.quantity:
                continue
            color = "-"
            if c.parts.color_id:
                color = c.parts.color_id.color_short
            need_to_cut.append({
                "parts": c.parts.id,
                "parts_name": str(c.parts.material_id.material_name),
                "parts_color": color,
                "length": c.length,
                "to_need_count": c.need_count - c.quantity
            })
        else:
            st = Stock.objects.filter(parts=c.parts.id)
            if not(st):
                need_to_order.append({
                    "parts": c.parts.id,
                    "parts_name": str(c.parts.material_id.material_name),
                    "parts_color": color,
                    "to_need_count": c.need_count
                })
            else:
                st = st[0]
                if st.quantity - c.need_count + c.quantity < 0:
                    c.quantity += st.quantity
                    c.save()
                    st.delete()
                    need_to_order.append({
                        "parts": c.parts.id,
                        "parts_name": str(c.parts.material_id.material_name),
                        "parts_color": color,
                        "to_need_count": c.need_count - c.quantity
                    })
                else:
                    ss = c.need_count + c.quantity
                    c.quantity += ss
                    st.quantity -= ss
                    c.save()
                    st.save()
                    if st.quantity == 0:
                        st.delete()
        
    
    if not(need_to_cut) and not(need_to_order):
        rollets[0].status_packed = True
        rollets[0].save()
        return JsonResponse({'status': 'ok'}, status=200)
    else:
        return JsonResponse({'status': 'not_ok', "need_to_cut": need_to_cut, 
                                                 "need_to_order": need_to_order}, status=200)



@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def composition_projects(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    # if request.method == 'POST':
    rollets = []
    compositions = []
    for i in request.data["project_ids"]:
        rollets += Rollets.objects.filter(project_id=i)
    for i in rollets:
        compositions += Composition.objects.filter(rollets_id=i.id)

    serializer = serializers.CompositionProjectSerializer(compositions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def materials_quantity(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    # if request.method == 'POST':
    rollets = []
    compositions = []
    parts = []
    materials = []
    for i in request.data["project_ids"]:
        rollets += Rollets.objects.filter(project_id=i)
    # for i in rollets:
    #     compositions += Composition.objects.filter(rollets_id=i.id)
    print(rollets)
    for i in rollets:
        parts += Parts.objects.filter(id=i.parts_id)
        compositions += Composition.objects.filter(rollets_id=i.id, parts=i.parts_id)
    print(parts, compositions)
    for i in parts:
        for j in compositions:
            le = Composition.objects.filter(parts=i.id, length=j.length)
            if len(le) > 0:
                print(len(le), le, i.material_id, j.length)
                materials.append(dict({"matrial_id": int(i.id),
                                       "material_length": int(j.length),
                                       "need_count": str(len(le))}))


    #serializer = serializers.CompositionProjectSerializer(compositions, many=True)
    return JsonResponse({'status': 'ok', "results": list(materials)})


@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def snippet_list_new(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    #if request.method == 'POST':
    rollets = []
    compositions = []
    for i in request.data["data"]:
        rollets += Rollets.objects.filter(project_id=i)
    print(rollets)
    for i in rollets:
        compositions += Composition.objects.filter(rollets_id=i.id, length__gt=0)
    
    result = dict()

    for c in compositions:
        if not(c.parts.id in result.keys()):
            color = Colors.objects.filter(id=c.parts.color_id_id)
            if not(color):
                data = {
                    "name": Materials.objects.filter(id=c.parts.material_id_id)[0].material_name,
                    "code": c.parts.id,
                    "data": []
                }
            else:
                data = {
                    "name": Materials.objects.filter(id=c.parts.material_id_id)[0].material_name,
                    "code": c.parts.id,
                    "color": Colors.objects.filter(id=c.parts.color_id_id)[0].color_name,
                    "color_short": Colors.objects.filter(id=c.parts.color_id_id)[0].color_short,
                    "data": []
                }
            result[c.parts.id] = data

        result[c.parts.id]["data"].append({
            "length": c.length,
            "need_count": c.need_count,
            "quantity": c.quantity
        })
    
    # res = result.items()[1]
    # print(result.values())


    return JsonResponse({'status': 'ok', "results": list(result.values())})
    # if serializer.is_valid():pass
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.data)#, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    # if request.method == 'GET':
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    # if request.method == 'POST':
    rollets = []
    compositions = []
    for i in request.data["data"]:
        rollets += Rollets.objects.filter(project_id=i)
    for i in rollets:
        compositions += Composition.objects.filter(rollets_id=i.id)

    serializer = serializers.CompositionSerializer(compositions, many=True)

    # if serializer.is_valid():pass
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    print("Hwllo")
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def cutting_new(request):
    rollets = []
    compositions = []
    stock_rests = {}
    need_rests = {}
    # print(request.data["project_ids"])
    for i in request.data["project_ids"]:
        rollets += Rollets.objects.filter(project_id=int(i))
    # print(rollets)
    for i in rollets:
        compositions += Composition.objects.filter(rollets_id=i.id, parts=request.data["material_id"])


    for i in compositions:
        if i.length in need_rests.keys():
            need_rests[i.length] += i.need_count
        else:
            need_rests[i.length] = i.need_count

    need_rests = [[k, need_rests[k]] for k in need_rests.keys()]

    st = Stock.objects.filter(parts=request.data["material_id"])

    for j in st:
        stock_rests[int(j.length)] = int(j.quantity)
    
        
    material_id = Parts.objects.filter(id=request.data["material_id"])[0].material_id.id
    default_lenght = Materials.objects.filter(id=material_id)[0].default_lenght
    good_cut = Materials.objects.filter(id=material_id)[0].good_cut


    # print(stock_rests)
    # print()
    # print(need_rests)
    # print()

    res_new, res_old = cutting(stock_rests, need_rests, default_lenght, good_cut)

    transform_new = [i for n, i in enumerate(res_new) if i not in res_new[n + 1:]]

    for t in transform_new:
        for r in res_new:
            if r["material"] == t["material"] and r["rest"] == t["rest"] and r["map"] == t["map"]:
                if "count" in t.keys():
                    t["count"] += 1
                else:
                    t["count"] = 1
    
    transform_old = [i for n, i in enumerate(res_old) if i not in res_old[n + 1:]]
    for t in transform_old:
        if not(t["map"]):
            transform_old.remove(t)


    for t in transform_old:
        for r in res_old:
            if r["material"] == t["material"] and r["rest"] == t["rest"] and r["map"] == t["map"]:
                if "count" in t.keys():
                    t["count"] += 1
                else:
                    t["count"] = 1

    #for i in transform_new:
    print(transform_new)
    #[{'material': 6000, 'rest': 1183, 'map': [2335, 1241, 1241], 'count': 1}, {'material': 6000, 'rest': 2895, 'map': [1235, 935, 935], 'count': 1}]
    #transform_new_new = transform_new.copy()
    for i in transform_new:
        queue = Queue.objects.filter(id=request.data["material_id"], length=i["material"])
        if len(queue) > 1:
            i["status"] = "ordered"
        else:
            i["status"] = "not ordered"
    print(transform_new)
    return JsonResponse({'status': 'ok', "results": {
        "res_new": transform_new,
        "res_old": transform_old,
    }}, status=200)



@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def add_queue(request):
    project_ids = request.data["project_ids"]
    material_id = request.data["material_id"]
    list_order = request.data["list_order"]

    for i in list_order:
        queue = Queue.objects.filter(parts_id=request.data["material_id"], length=i["material"])
        if len(queue) > 1:
            i["status"] = "already booked"
        else:
            i["status"] = "ordered"
            params = {
                "quantity": i["count"],
                "length": i["material"],
                "parts_id": material_id
            }
            # print(t[0].id)
            queue = Queue.objects.create(**params)
            for j in project_ids:
                queue.project.add(int(j))

    return JsonResponse({'status': 'ok', "results": {
        "list": list_order
    }}, status=200)


@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def get_queue(request):
    #project_ids = request.data["project_ids"]
    material_id = request.data["material_id"]
    #list_order = request.data["list_order"]

    #queue = []

    queue = Queue.objects.filter(parts_id=material_id)
    serializer = serializers.QueueSerializer(queue, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def queue(request):
    #project_ids = request.data["project_ids"]
    #material_id = request.data["material_id"]
    #list_order = request.data["list_order"]

    #queue = []

    queue = Queue.objects.filter()
    serializer = serializers.QueueSerializer(queue, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def del_queue(request):
    #project_ids = request.data["project_ids"]
    material_id = request.data["material_id"]
    list_order = request.data["list"]
    list_new = list_order.copy()
    for i in enumerate(list_order):
        queue = Queue.objects.filter(parts_id=material_id, length=i[1]["material"])
        if len(queue) > 0:
            #i["status"] = "already booked"
            if i[1]["status"]:
                if i[1]["material"] != 0:
                    result = requests.post(f'http://127.0.0.1:8000/api/add_material_stock',
                                           json={'material_id': material_id, 'quantity': i[1]['quantity'],
                                                 'length': i[1]["material"]})
                else:
                    result = requests.post(f'http://127.0.0.1:8000/api/add_material_stock',
                                           json={'material_id': material_id, 'quantity': i[1]['quantity']})
            if queue[0].quantity - i[1]["quantity"] <= 0:
                list_new.pop(i[0])
                queue[0].delete()
            else:
                list_new[i[0]]["quantity"] = queue[0].quantity - i[1]["quantity"]
                queue[0].quantity = queue[0].quantity - i[1]["quantity"]
                queue[0].save()
        else:
            pass
            # i["status"] = "ordered"
            # params = {
            #     "quantity": i["count"],
            #     "length": i["material"],
            #     "parts_id": material_id
            # }
            # # print(t[0].id)
            # queue = Queue.objects.create(**params)
            # for j in project_ids:
            #     queue.project.add(int(j))

    return JsonResponse({'status': 'ok', "results": {
        "list": list_new
    }}, status=200)


@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def cutting_save(request):

    # TODO: save rests after cutting (и запись отпиленных в значения quintity)
    # {"material_id": 4131, "project_ids":[1,2], "length":1366, "map":[800, 200], "quantity": 1}

    material_id = request.data["material_id"]
    length = request.data["length"]
    map = request.data["map"]
    quantity = request.data["quantity"]
    res = []
    #materials = Materials.objects.filter(id=material_id)

    rollets = []
    compositions = []
    compositions_rests = []
    stock = {}
    materials = []
    parts = []
    length_new = 0
    material_name = ""

    for i in request.data["project_ids"]:
        rollets += Rollets.objects.filter(project_id=i)
    # for i in rollets:
    #     compositions += Composition.objects.filter(rollets_id=i.id)

    # for i in compositions:
    parts += Parts.objects.filter(id=material_id) #id=i.parts_id)

    #material_name = Materials.objects.filter(id=material_id)
    #print(material_name)

    material_name = Materials.objects.filter(id=parts[0].material_id_id)
    material_name = material_name[0].material_name

    #print(parts)
    for i in parts:
        t = Stock.objects.filter(parts=i.id, length=length)
        if len(t) > 0:
            #print("test")
            #for j in t:
                #length_new = j.length - sum(map)
            #t[0].length = length - sum(map)
            t[0].quantity -= quantity
            t[0].save()
            # params = {
            #     'length': length - sum(map),
            #     'quantity': quantity,
            #     'parts_id': i.id,
            #     'shelf_id': 1,
            #     'barcode': 1
            # }
            # Stock.objects.create(**params)
        else:
            # return JsonResponse({'status': 'error',
            #                      "error_msg": "Нет остатков на складе, "
            #                                   "неправильный параметр длинны length для материала parts_number"},
            #                     status=200)
            params = {
                'length': length - sum(map),
                'quantity': quantity,
                'parts_id': i.id,
                'shelf_id': 1,
                'barcode': 1
            }
            Stock.objects.create(**params)

        for m in rollets:
            for k in map:  # Что делать с map, ведь мы по нему не ищем?
                com = Composition.objects.filter(parts=i.id, length=k, rollets_id=m.id)
                #print(com)
                if len(com) > 0:
                    for j in com:
                        #length_new = j.length
                        j.quantity += quantity
                        j.save()

                # params = {
                #     'length': length,
                #     'need_count': k,
                #     'quantity': 1,
                #     'parts_id': i.id
                # }
                # Composition.objects.create(**params)
        #for j in Composition.objects.filter(parts=i.id):

    print(material_name, parts[0], length - sum(map))
    return JsonResponse({'status': 'ok', "saved_rests": [{
        "name": material_name,
        "parts_number": parts[0].id,
        "length": length - sum(map),
        "quantity": quantity
    }]}, status=200)


@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def cutting_remove(request):

    # TODO: save rests after cutting (и запись отпиленных в значения quintity)
    # {"material_id": 4131, "project_ids":[1,2], "length":1366, "map":[800, 200], "quantity": 1}

    material_id = request.data["material_id"]
    length = request.data["length"]
    map = request.data["map"]
    quantity = request.data["quantity"]
    res = []
    # materials = Materials.objects.filter(id=material_id)

    rollets = []
    compositions = []
    compositions_rests = []
    stock = {}
    materials = []
    parts = []
    length_new = 0
    material_name = ""

    for i in request.data["project_ids"]:
        rollets += Rollets.objects.filter(project_id=i)
    # for i in rollets:
    #     compositions += Composition.objects.filter(rollets_id=i.id)

    # for i in compositions:
    parts += Parts.objects.filter(id=material_id)  # id=i.parts_id)

    # material_name = Materials.objects.filter(id=material_id)
    # print(material_name)

    material_name = Materials.objects.filter(id=parts[0].material_id_id)
    material_name = material_name[0].material_name

    # print(parts)
    for i in parts:
        t = Stock.objects.filter(parts=i.id, length=length)
        if len(t) > 0:
            t[0].quantity += quantity
            t[0].save()
            #t[0].delete()
        t_new = Stock.objects.filter(parts=i.id, length=length - sum(map))
        if len(t_new) > 0:
            t_new[0].quantity += quantity
            t_new[0].save()
        for m in rollets:
            for k in map:
                com = Composition.objects.filter(parts=i.id, length=k, rollets_id=m.id)
                # print(com)
                if len(com) > 0:
                    for j in com:
                        # length_new = j.length
                        j.quantity -= 1
                        j.save()

    return JsonResponse({'status': 'ok', "remove_rests": [{
        "name": material_name,
        "parts_number": parts[0].id,
        "length": length,
        "quantity": request.data["quantity"]
    }]}, status=200)



@api_view(['POST'])
@permission_classes([ManagerAllEditOrReadOnly])
@base_view
def defect_cutting(request):

    # TODO: save rests after cutting (и запись отпиленных в значения quintity)
    # {"material_id": 4131, "project_ids":[1,2], "length":1366, "map":[800, 200], "quantity": 1}

    material_id = request.data["material_id"]
    #length = request.data["length"]
    map = request.data["map"]
    quantity = request.data["quantity"]
    project_ids = request.data["project_ids"]
    rest = request.data["rest"]
    res = []
    # materials = Materials.objects.filter(id=material_id)

    rollets = []
    compositions = []
    compositions_rests = []
    stock = {}
    materials = []
    parts = []
    length_new = 0
    material_name = ""

    for i in request.data["project_ids"]:
        rollets += Rollets.objects.filter(project_id=i)
    # for i in rollets:
    #     compositions += Composition.objects.filter(rollets_id=i.id)

    # for i in compositions:
    parts += Parts.objects.filter(id=material_id)  # id=i.parts_id)

    # material_name = Materials.objects.filter(id=material_id)
    # print(material_name)

    material_name = Materials.objects.filter(id=parts[0].material_id_id)
    material_name = material_name[0].material_name

    # print(parts)
    for i in parts:
        t = Stock.objects.filter(parts=i.id, length=rest)
        if len(t) > 0:
            # print("test")
            # for j in t:
            # length_new = j.length - sum(map)
            # t[0].length = length - sum(map)
            t[0].quantity += 1
            t[0].save()
            # params = {
            #     'length': length - sum(map),
            #     'quantity': quantity,
            #     'parts_id': i.id,
            #     'shelf_id': 1,
            #     'barcode': 1
            # }
            # Stock.objects.create(**params)
        else:
            # return JsonResponse({'status': 'error',
            #                      "error_msg": "Нет остатков на складе, "
            #                                   "неправильный параметр длинны length для материала parts_number"},
            #                     status=200)
            params = {
                'length': rest,
                'quantity': 1,
                'parts_id': i.id,
                'shelf_id': 1,
                'barcode': 1
            }
            Stock.objects.create(**params)

        for m in rollets:
            for k in map:  # Что делать с map, ведь мы по нему не ищем?
                com = Composition.objects.filter(parts=i.id, length=k, rollets_id=m.id)
                # print(com)
                if len(com) > 0:
                    for j in com:
                        # length_new = j.length
                        j.quantity += quantity
                        j.save()

                # params = {
                #     'length': length,
                #     'need_count': k,
                #     'quantity': 1,
                #     'parts_id': i.id
                # }
                # Composition.objects.create(**params)
        # for j in Composition.objects.filter(parts=i.id):

    #print(material_name, parts[0], length - sum(map))
    return JsonResponse({'status': 'ok', "saved_rests": [{
        "name": material_name,
        "parts_number": parts[0].id,
        "length": rest,
        "quantity": quantity
    }]}, status=200)



@api_view(['POST'])
@permission_classes([WorkerAllEditOrReadOnly])
@base_view
def lengths_accessories(request):

    # TODO: save rests after cutting (и запись отпиленных в значения quintity)
    # {"material_id": 4131, "project_ids":[1,2], "length":1366, "map":[800, 200], "quantity": 1}

    material_type = request.data["material_type"]
    res = []
    #materials = Materials.objects.filter(id=material_id)

    res = []
    if material_type == "lengths":
        mm = Materials.objects.filter()
        for i in mm:
            try:
                if i.default_lenght > 0:
                    cl = Classes.objects.filter(id=i.class_id_id)

                    #print(cl)

                    dim = DIM.objects.filter(id=cl[0].dim_id)

                    #print(dim)

                    pa = Parts.objects.filter(material_id_id=i.id)

                    #print(pa)

                    sto = Stock.objects.filter(parts_id=pa[0].id)

                    #print(sto)

                    res.append({"material_name": i.material_name,
                                "default_lenght": i.default_lenght,
                                "dim": dim[0].dim,
                                "quantity": sto[0].quantity})
            except:pass
                #return JsonResponse({'status': 'ok'}, status=200)
                #print("error")
        sto = Stock.objects.filter()
        for i in sto:
            if i.length > 0:
                pa = Parts.objects.filter(id=i.parts_id)
                #print(pa)
                mm = Materials.objects.filter(id=pa[0].material_id_id)
                #print(mm)
                cl = Classes.objects.filter(id=mm[0].class_id_id)

                dim = DIM.objects.filter(id=cl[0].dim_id)
                res.append({"material_name": mm[0].material_name,
                            "dim": dim[0].dim,
                            "default_lenght": mm[0].default_lenght,
                            "quantity": i.quantity})
    elif material_type == "accessories":
        mm = Materials.objects.filter()
        for i in mm:
            try:
                if i.default_lenght == 0:
                    cl = Classes.objects.filter(id=i.class_id_id)

                    dim = DIM.objects.filter(id=cl[0].dim_id)

                    pa = Parts.objects.filter(id=i.id)

                    #print(pa)
                    #return JsonResponse({'status': 'ok'}, status=200)
                    sto = Stock.objects.filter(parts_id=pa[0].id)

                    res.append({"material_name": i.material_name,
                                "dim": dim[0].dim,
                                "quantity": sto[0].quantity})
            except:pass
        sto = Stock.objects.filter()
        for i in sto:
            if i.length == 0:
                pa = Parts.objects.filter(id=i.parts_id)
                #print(pa)
                mm = Materials.objects.filter(material_name_id=pa[0].material_id_id)
                #print(mm)
                cl = Classes.objects.filter(id=mm[0].class_id_id)

                dim = DIM.objects.filter(id=cl[0].dim_id)
                res.append({"material_name": mm[0].material_name,
                            "dim": dim[0].dim,
                            "quantity": i.quantity})


    return JsonResponse({'status': 'ok', "results": list(res)}, status=200)



@api_view(['POST'])
@permission_classes([WorkerAllEditOrReadOnly])
@base_view
def lengths_search(request):
    length = 0
    #if "length" in request.data.keys():
    length = request.data["length"]

    material_id = request.data.get("material_id")
    res = []
    if material_id:
        pa = Parts.objects.filter(id=material_id)
        sto = Stock.objects.filter(length__gt=length, parts_id=pa[0].id)
        for i in sto:
            filename = i.image
            if filename == "0":
                i.save()
                filename = i.image

            # short_report = open(f"media/{filename}", 'rb')
            # report_encoded = base64.b64encode(short_report.read())
            #
            # report_encoded = str(report_encoded).replace("b'", "")
            # report_encoded = report_encoded.replace("'", "")

            res.append({
                "name": str(pa[0].material_id),
                "color": str(pa[0].color_id),
                "partcode": material_id,
                "length": i.length,
                "count": i.quantity,
                "barcode": "{'stock_id':" + str(sto[0].id) + "{'parts':" + str(pa[0].id) + "}}"#str(report_encoded),
                })
    else:
        sto = Stock.objects.filter(length__gt=length)
        for i in sto:
            filename = i.image
            if filename == "0":
                i.save()
                filename = i.image

            # short_report = open(f"media/{filename}", 'rb')
            # report_encoded = base64.b64encode(short_report.read())
            #
            # report_encoded = str(report_encoded).replace("b'", "")
            # report_encoded = report_encoded.replace("'", "")

            res.append({
                "name": str(i.parts.material_id),
                "color": str(i.parts.color_id),
                "partcode": i.parts_id,
                "length": i.length,
                "count": i.quantity,
                "barcode": "{'stock_id':" + str(sto[0].id) + "{'parts':" + str(sto[0].parts_id) + "}}"
                })
    return JsonResponse({'status': 'ok', "results": list(res)})


@api_view(['POST'])
@permission_classes([WorkerAllEditOrReadOnly])
@base_view
def accessories_search(request):

    material_id = request.data.get("material_id")
    res = []
    if material_id:
        pa = Parts.objects.filter(id=material_id)
        sto = Stock.objects.filter(length=0, parts_id=pa[0].id)
        for i in sto:
            res.append({
                "name": str(pa[0].material_id),
                "color": str(pa[0].color_id),
                "partcode": material_id,
                "count": i.quantity,
                "barcode": i.barcode,
                })
    else:
        sto = Stock.objects.filter(length=0)
        # print(len(sto))
        for i in sto:
            res.append({
                "name": str(i.parts.material_id),
                "color": str(i.parts.color_id),
                "partcode": i.parts_id,
                "count": i.quantity,
                "barcode" : i.barcode,
                })
        # print(len(res))
    return JsonResponse({'status': 'ok', "results": list(res)})


@api_view(['POST'])
@permission_classes([WorkerAllEditOrReadOnly])
@base_view
def show_materials_in_stock(request):
    
    res = []
    material_type = request.data["material_type"]

    sto = None
    
    if material_type=="lengths":
        sto = Stock.objects.filter(~Q(length=0))
    elif material_type=="accessories":
        sto = Stock.objects.filter(length=0)
    else:
        return JsonResponse({'status': 'error', "description":"\"material_type\" must be \'lengths\' or \'accessories'"})

    parts = []

    for s in sto:
        if s.parts.id in parts:
            continue
        else:
            parts.append(s.parts.id)

        color = "без цвета"
        if s.parts.color_id:
            color = s.parts.color_id.color_short
        
        res.append({
            "name": str(s.parts.material_id),
            "partcode": s.parts.id,
            "color": color
        })

    return JsonResponse({'status': 'ok', "results": list(res)})


@api_view(['POST'])
@permission_classes([WorkerAllEditOrReadOnly])
@base_view
def add_material_stock(request):
    data = json.loads(request.body)
    length = data.get("length")
    material_id = data.get("material_id")
    quantity = data.get("quantity")
    res = []

    if length:
        stock = Stock.objects.filter(parts_id=int(material_id), length=length)
    else:
        stock = Stock.objects.filter(parts_id=int(material_id), length=0)
    if len(stock) > 0:
        # parts = Parts.objects.filter(id=int(material_id))
        # serializer = serializers.PartsSerializer(parts, many=True)
        # #return Response(serializer.data)
        # qr_code = {
        #     "length": length,
        #     "box_number": 1,
        #     "cell_number": 1,
        #     "parts": serializer.data
        # }  # Длина, цвет, название материала, артикуль, номер полки
        # js = json.dumps(qr_code)
        #
        # filename = "site.png"
        # img = qrcode.make(js)
        # img.save(filename)


        stock[0].quantity += int(quantity)
        stock[0].save()

        filename = stock[0].image

        # short_report = open(f"media/{filename}", 'rb')
        # report_encoded = base64.b64encode(short_report.read())
        #
        # report_encoded = str(report_encoded).replace("b'", "")
        # report_encoded = report_encoded.replace("'", "")"barcode": "{'stock_id':" + str(sto[0].id) + "{'parts':" + str(sto[0].parts_id) + "}}"

        if length:
            return JsonResponse({'status': 'ok', 'results': {
                'material_id': material_id,
                'quantity': stock[0].quantity,
                'length': length,
                "qr_code": "{'stock_id':" + str(stock[0].id) + "{'parts':" + str(stock[0].parts_id) + "}}"
            }})
        else:
            return JsonResponse({'status': 'ok', 'results': {
                'material_id': material_id,
                'quantity': stock[0].quantity,
                "qr_code": "{'stock_id':" + str(stock[0].id) + "{'parts':" + str(stock[0].parts_id) + "}}"
            }})

    shelf = Shelf.objects.filter()
    for i in shelf:
        shelf_stock = Stock.objects.filter(shelf_id=int(i.id))
        if len(shelf_stock):
            if i.cell_number < 4:
                params = {
                    'box_number': i.box_number,
                    'cell_number': i.cell_number + 1,
                }
                Shelf.objects.create(**params)
                shelf = Shelf.objects.filter(box_number=i.box_number, cell_number=i.cell_number)
            else:
                params = {
                    'box_number': i.box_number + 1,
                    'cell_number': 1,
                }
                Shelf.objects.create(**params)
                shelf = Shelf.objects.filter(box_number=i.box_number, cell_number=i.cell_number)
    if length:
        params = {
            'quantity': quantity,
            'length': length,
            'barcode': 1,
            'shelf_id': shelf[0].id,
            'parts_id': int(material_id)
        }
    else:
        params = {
            'quantity': quantity,
            'length': 0,
            'barcode': 1,
            'shelf_id': shelf[0].id,
            'parts_id': int(material_id)
        }
    # print(t[0].id)
    stock = Stock.objects.create(**params)
    # if material_id:
    #     pa = Parts.objects.filter(id=material_id)
    #     sto = Stock.objects.filter(length__gt=length, parts_id=pa[0].id)
    #     for i in sto:
    #         res.append({
    #             "name": str(pa[0].material_id),
    #             "color": str(pa[0].color_id),
    #             "partcode": material_id,
    #             "length": i.length,
    #             "count": i.quantity,
    #             "barcode" : i.barcode,
    #             })
    # else:
    #     sto = Stock.objects.filter(length__gt=length)
    #     for i in sto:
    #         res.append({
    #             "name": str(sto[0].parts.material_id),
    #             "color": str(sto[0].parts.color_id),
    #             "partcode": sto[0].parts_id,
    #             "length": i.length,
    #             "count": i.quantity,
    #             "barcode" : i.barcode,
    #             })
    # sto = Stock.objects.filter(id=stock.id)
    # filename = sto[0].image
    #
    # short_report = open(f"media/{filename}", 'rb')
    # report_encoded = base64.b64encode(short_report.read())
    #
    # report_encoded = str(report_encoded).replace("b'", "")
    # report_encoded = report_encoded.replace("'", "")

    if length > 0:
        return JsonResponse({'status': 'ok', 'results': {
            'material_id': material_id,
            'quantity': quantity,
            'length': length,
            "qr_code": "{'stock_id':" + str(stock[0].id) + "{'parts':" + str(stock[0].parts_id) + "}}"
        }})
    else:
        return JsonResponse({'status': 'ok', 'results': {
            'material_id': material_id,
            'quantity': quantity,
            "qr_code": "{'stock_id':" + str(stock[0].id) + "{'parts':" + str(stock[0].parts_id) + "}}"
        }})


@api_view(['POST'])
@permission_classes([WorkerAllEditOrReadOnly])
@base_view
def delete_material_stock(request):
    length = request.data.get("length")
    material_id = request.data.get("material_id")
    quantity = request.data.get("quantity")
    res = []

    if length:
        stock = Stock.objects.filter(parts_id=int(material_id), length=length)
        if len(stock) > 0:
            stock[0].quantity -= int(quantity)
            stock[0].save()
            return JsonResponse({'status': 'ok', 
                                'results': {
                                    'material_id': material_id,
                                    'quantity': stock[0].quantity,
                                    'length': length
                                }})
    else:
        stock = Stock.objects.filter(parts_id=int(material_id), length=0)
        if len(stock) > 0:
            stock[0].quantity -= int(quantity)
            stock[0].save()
        return JsonResponse({'status': 'ok', 
                             'results': {
                                'material_id': material_id,
                                'quantity': stock[0].quantity
                             }})

    # shelf = Shelf.objects.filter()
    # #pa = Parts.objects.filter(artnumber=int(i['partcode']))
    # params = {
    #     'quantity': quantity,
    #     'length': length,
    #     'barcode': 1,
    #     'shelf_id': shelf[0].id,
    #     'parts_id': int(material_id)
    # }
    # # print(t[0].id)
    # Stock.objects.create(**params)
    # if material_id:
    #     pa = Parts.objects.filter(id=material_id)
    #     sto = Stock.objects.filter(length__gt=length, parts_id=pa[0].id)
    #     for i in sto:
    #         res.append({
    #             "name": str(pa[0].material_id),
    #             "color": str(pa[0].color_id),
    #             "partcode": material_id,
    #             "length": i.length,
    #             "count": i.quantity,
    #             "barcode" : i.barcode,
    #             })
    # else:
    #     sto = Stock.objects.filter(length__gt=length)
    #     for i in sto:
    #         res.append({
    #             "name": str(sto[0].parts.material_id),
    #             "color": str(sto[0].parts.color_id),
    #             "partcode": sto[0].parts_id,
    #             "length": i.length,
    #             "count": i.quantity,
    #             "barcode" : i.barcode,
    #             })
    return JsonResponse({'status': 'ok'})



@api_view(['POST'])
@permission_classes([WorkerAllEditOrReadOnly])
@base_view
def add_materials(request):
    materials = request.data["materials"]
    added = []
    for m in materials:
        print(m["partcode"], m["count"], m["length"])
        part = Parts.objects.filter(artnumber=m["partcode"])[0]

        stoks = Stock.objects.filter(length=m["length"], parts=part.id)
        print(stoks)
        if len(stoks) > 0:
            stoks[0].quantity += m["count"]
            stoks[0].save()
        else:
            c = Shelf.objects.filter()[0]
            params = {
                    'quantity': m["count"],
                    'length': m["length"],
                    'barcode': 1,
                    'shelf': c,
                    'parts': part,
                }
            added.append(params)
            stock = Stock.objects.create(**params)


    return JsonResponse({'status': 'ok', 'response': "ok"})


# @csrf_exempt
@base_view
def api_get_projects(request):
    if request.method == 'POST':
        #results = request.POST
        #data = json.loads(request.body)

        # t = Project.objects.filter()


        return JsonResponse({'status': 'ok'}, status=200)



# @csrf_exempt
def api_add_colors(request):
    if request.method == 'POST':
        #results = request.POST
        data = json.loads(request.body)
        #print(data)
        for i in data["list"]:

            if i[4] == 'None':
                i[4] = 0
            if i[0] == 'None':
                i[0] = 0
            params = {
                'color_name': i[1],
                'color_short': i[2],
                'rgb': i[3],
                'ral': i[4],
                'color_alutech': i[0]
            }
            device = Colors.objects.create(**params)
        return JsonResponse({'status': 'ok'}, status=200)

# @csrf_exempt
def api_add_dim(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for i in data["list"]:

            if i[1] == 'False':
                i[1] = False
            else:
                i[1] = True
            params = {
                'dim': i[0],
                'can_cut': i[1],
            }
            device = DIM.objects.create(**params)
        return JsonResponse({'status': 'ok'}, status=200)

# @csrf_exempt
def api_add_classes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for i in data["list"]:
            try:
                t = DIM.objects.filter(dim=i[1])
                params = {
                    'class_name': i[0],
                    'dim_id': t[0].id
                }
                device = Classes.objects.create(**params)
            except:
                continue
        return JsonResponse({'status': 'ok'}, status=200)


# @csrf_exempt
def api_add_materials(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for i in data["list"]:
            try:
                t = Classes.objects.filter(class_name=i[0])
                print(t[0].id)
                if i[2] == "null":
                    i[2] = 0
                params = {
                    'material_name': i[1],
                    'class_id_id': t[0].id,
                    'weight': i[2],
                    'default_lenght': 0,
                    'good_cut': 0,
                }
                device = Materials.objects.create(**params)
            except:
                print(i, traceback.format_exc())
                continue
        return JsonResponse({'status': 'ok'}, status=200)

# @csrf_exempt
def api_add_parts(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sp = []
        for i in data["list"]:
            try:
                m = Materials.objects.filter(material_name=i[0])
                if i[1] != "None" and i[1] != "N" and i[1] != "00":
                    c = Colors.objects.filter(color_alutech=i[1])
                    params = {
                        'material_id_id': m[0].id,
                        'artnumber': i[2],
                        'color_id_id': c[0].id,
                        'price': i[3],
                    }
                else:
                    params = {
                        'material_id_id': m[0].id,
                        'artnumber': i[2],
                        'price': i[3],
                    }
                #print(t[0].id)
                device = Parts.objects.create(**params)
            except:
                sp.append(i[0])
                print(i, traceback.format_exc())
                continue
        print(sp)

        return JsonResponse({'status': 'ok'}, status=200)


# @csrf_exempt
def api_add_rolls(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #project_id = data["material_partcode"]
        #parts_id = data["cutting_data"]
        #material_partcode = data["list"]["material_partcode"]
        #print(data)
        sp = []
        sp_date = []
        receipt_date = datetime.now().date()
        #a = '2020-12-12'
        #print(receipt_date)
        dt = datetime.strptime(str(receipt_date), '%Y-%m-%d')
        deadline_date = dt + timedelta(days=3)
        params = {
            'receipt_date': receipt_date,
            'deadline_date': deadline_date,
            'status_id': 2
        }
        # print(t[0].id)
        sp_new = []
        pro = Project.objects.create(**params)
        #pro = Project.objects.filter(receipt_date=receipt_date, deadline_date=deadline_date, status_id=2)
        #sp = []
        for i in data["list"]:
            #print(i)
            try:
                r = Parts.objects.filter(artnumber=int(i["material_partcode"]))
                #p = Project.objects.filter(artnumber=int(i[1]))
                # rol = Rollets.objects.filter(width=i["width"],
                #                              height=i["height"],
                #                              project_id=pro.id,
                #                              parts_id=r[0].id)
                #if len(rol) == 0:
                params = {
                    'width': i["width"],
                    'height': i["height"],
                    'project_id': pro.id,
                    'parts_id': r[0].id
                }
                #print(t[0].id)
                rr = Rollets.objects.create(**params)

                #print(rr.id)
                # ro = Rollets.objects.filter(project_id=pro.id,
                #                             parts_id=r[0].id,
                #                             width=i["width"],
                #                             height=i["height"])
                ro = rr.id
            except:
                sp.append(i)
                print(i, traceback.format_exc())
                continue
            for j in i["cutting_data"]:
                #sp_new
                print(j)
                try:
                    #r = Rollets.objects.filter(id=i[0])
                    p = Parts.objects.filter(artnumber=int(j["partcode"]))
                    params = {
                        'parts_id': p[0].id,
                        'rollets_id': ro,
                        'length': j["length"],
                        'need_count': j["count"],
                        'quantity': 0
                    }
                    # print(t[0].id)
                    device = Composition.objects.create(**params)
                except:
                    sp.append(i)
                    print(i, traceback.format_exc())
                    continue
        # #print(sp)

        return JsonResponse({'status': 'ok'}, status=200)


# @csrf_exempt
def api_add_composition(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sp = []
        for i in data["list"]:
            try:
                r = Rollets.objects.filter(id=i[0])
                p = Parts.objects.filter(artnumber=int(i[1]))
                params = {
                    'parts_id': p[0].id,
                    'rollets_id': r[0].id,
                    'length': i[2],
                    'need_count': i[3],
                    'quantity': 0
                }
                #print(t[0].id)
                device = Composition.objects.create(**params)
            except:
                sp.append(i[0])
                print(i, traceback.format_exc())
                continue
        #print(sp)

        return JsonResponse({'status': 'ok'}, status=200)

# @csrf_exempt
def api_add_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sp = []
        for i in data["list"]:
            try:
                #r = Rollets.objects.filter(id=i[0])
                #p = Parts.objects.filter(artnumber=int(i[1]))
                shelf = Shelf.objects.filter()
                pa = Parts.objects.filter(artnumber=int(i['partcode']))
                stock = Stock.objects.filter(parts_id=pa[0].id, length=int(i['length']))
                if len(stock) > 0:
                    stock[0].quantity += int(i['count'])
                    stock[0].save()
                else:
                    params = {
                        'quantity': int(i['count']),
                        'length': int(i['length']),
                        'barcode': 1,
                        'shelf_id': shelf[0].id,
                        'parts_id': pa[0].id
                    }
                    #print(t[0].id)
                    device = Stock.objects.create(**params)
            except:
                sp.append(i)
                print(i, traceback.format_exc())
                continue
        #print(sp)

        return JsonResponse({'status': 'ok'}, status=200)

