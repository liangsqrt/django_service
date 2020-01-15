from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import SchoolFilterSerializer
from .models import SchoolOverViewItem
# Create your views here.


class SchooleFilter(APIView):
    queryset = SchoolOverViewItem.objects.all()
    serializer_class = SchoolFilterSerializer  # 这个字段这里连validate都不用验证，我觉得可以去掉。
    
    def post(self, request, *args, **kwargs):
        print(request)

    def get(self, request, *args, **kwargs):
        self.queryset
        print(request)
