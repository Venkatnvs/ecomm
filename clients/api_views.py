from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

@api_view(['GET'])
def UserViewSet(request):
    queryset = User.objects.all().order_by('-date_joined')
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)