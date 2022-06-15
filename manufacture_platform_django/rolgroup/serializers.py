from rest_framework import serializers
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
#from .models import userProfile
#from .serializers import userProfileSerializer
from .license import IsOwnerProfileOrReadOnly
from .models import *


class userProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = userProfile
        fields = '__all__'




class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ('color_name', 'color_short')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('name_status', )


class ProjectSerializer(serializers.ModelSerializer):
    #status = serializers.SlugRelatedField()
    status_name = serializers.CharField(source='status.name_status')
    class Meta:
        model = Project
        fields = ('id', 'receipt_date', 'deadline_date', 'status_name', 'status')


class CompositionSerializer(serializers.ModelSerializer):
    # parts_material_id = serializers.CharField(source='parts.material_id')
    # parts_color_id = serializers.CharField(source='parts.color_id')
    # rollets_width = serializers.CharField(source='rollets.width')
    # rollets_height = serializers.CharField(source='rollets.height')

    # def _is_my_find(self, obj):
    #     print(self.data)
    #     parts_id = self.data.get("data")
    #     print(parts_id)
    #     # if user_id:
    #     #     return user_id in obj.my_objects.values_list("user_id", flat=True)
    #     return False


    class Meta:
        model = Composition
        depth = 1
        fields = ('id', 'length', 'need_count', 'quantity',
                  'parts', 'rollets', 'parts')

        # fieldsets = ('count', 'next', 'previous',
        #     ('results', {
        #         'fields': ('id', 'length', 'need_count', 'quantity',
        #           'parts_name', 'parts_color_id', 'rollets_width', 'rollets_height',
        #           'parts', 'rollets')
        #     }),
            # ('ID', {
            #     'fields': ('id_group', 'peer_id', 'peer_id_new')
            # }),
            # ('Статусы', {
            #     'fields': ('bol', 'bol_peer_id',)
            # }),
        # )


class CompositionProjectSerializer(serializers.ModelSerializer):
    composition_length = serializers.IntegerField(source='length')
    composition_need_count = serializers.IntegerField(source='need_count')
    composition_quantity = serializers.IntegerField(source='quantity')
    class Meta:
        model = Composition
        #depth = 1
        fields = ('id', 'composition_length', 'composition_need_count', 'composition_quantity')



class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'quantity', 'length', 'barcode', 'shelf', 'parts')


class RolletsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rollets
        fields = ('id', 'width', 'height', 'project', 'parts', 'status_packed')


class PartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parts
        depth = 1
        fields = ('id', 'material_id', 'artnumber', 'color_id')



class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        depth = 1
        fields = ('id', 'quantity', 'length', 'parts', 'project')
