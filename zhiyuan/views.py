from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SchoolFilterSerializer
from .models import SchoolOverViewItem
from rest_framework.response import Response
import json
# Create your views here.


class SchooleFilter(APIView):
    queryset = SchoolOverViewItem.objects.all()
    serializer_class = SchoolFilterSerializer  # 这个字段这里连validate都不用验证，我觉得可以去掉。
    
    def post(self, request, *args, **kwargs):
        print(request)

    def get(self, request, *args, **kwargs):
        province_list = self.queryset.values("province").distinct()
        is_985 = [0,1]
        school_types_list = self.queryset.values("school_types").distinct()
        tags_list = self.queryset.values("tags").distinct()
        result = {
            "province": [x["province"] for x in province_list],
            "is_985": is_985,
            "school_types": [x["school_types"] for x in school_types_list],
            "tags": [x["tags"] for x in tags_list]
        }
        self.queryset
        print(request)
        return Response(data=json.dumps(result))