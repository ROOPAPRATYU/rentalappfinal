from .serializers import CurrentUserPropertySerialzer,ImportSerializer
from accounts.models import User
from rest_framework.permissions import AllowAny
from . permissions import OwnerOrReadObly
from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, APIView
from .serializers import ProperySerializer
from .models import PropertyDetail
from rest_framework.parsers import MultiPartParser,FormParser
import pandas as pd
from django.http import FileResponse
from notification.tasks import send_mail_to_owner
from .models import PropertyDetail,Image
from .serializers import ProperySerializer,ImageSerializer,Propertyserializer

# Create your views here.


class PropertyPostListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ProperySerializer
    queryset = PropertyDetail.objects.all()
    
    def get(self, request:Request, pk=None):
        if pk:
            return self.retrieve(self, pk=pk)
        return self.list(request)
    
class ProperyPostView(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class =ProperySerializer
    
    permission_classes = [IsAuthenticated]
    def post(self, request:Request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
    
        if serializer.is_valid():
            serializer.save(owner=request.user)
    
            serializer.save()
            response = {
                "message": "Propery Details Submitted Successfylly",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message":serializer.errors
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated, OwnerOrReadObly])
def get_properties_for_current_user(request: Request):
    user = request.user
    serializer = CurrentUserPropertySerialzer(
        instance=user, context={"request": request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


class PropertyUpdateApiView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = Propertyserializer
    queryset = PropertyDetail.objects.all()

    
    def put(self, request: Request, *args, **kwargs):
        return self.update(request,*args, **kwargs)
    
    def get(self,request:Request,pk=None,*args,**kwargs):
        return self.retrieve(request,pk,*args,**kwargs)


class PropertyDeleteApiView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class =Propertyserializer
    queryset = PropertyDetail.objects.all()
    permission_classes = [IsAuthenticated]
    def delete(self, request: Request,*args, **kwargs):

        return self.destroy(request,*args, **kwargs)



class PropertyImportExportview(generics.GenericAPIView):
    serializer_class=ProperySerializer
    def get(self,request:Request,*args,**kwargs):
        property_obj=PropertyDetail.objects.all()
        serialize=ProperySerializer(property_obj,many=True)
        df=pd.DataFrame(serialize.data)
        excel_file = "output1.xlsx"
        df.to_excel(excel_file)
        response = FileResponse(open(excel_file, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="output1.xlsx"'
        return response
    
class propertyexportview(generics.GenericAPIView):
    serializer_class=ImportSerializer
    def post(self,request:Request,*args,**kwargs):
        serialize=self.serializer_class(data=request.data)
        if serialize.is_valid():
            file=serialize.validated_data.get("file")
            reader=pd.read_excel(file)
            reader.drop_duplicates(subset=["phone_number","adhar_num"],keep="last",inplace=True)
            
            for fields in (reader.values.tolist()):
                filter_data=PropertyDetail.objects.filter(phone_number=fields[8],adhar_num=fields[11])
                if filter_data.exists():
                   continue
                else:
                    PropertyDetail.objects.create(
                        owner=request.user,
                        property_name=fields[2],
                        email=fields[3],
                        tenant_name=fields[4], 
                        address=fields[5],
                        bhk=fields[6],
                        age=fields[7],
                        phone_number=fields[8],
                        rent=fields[9],
                        rent_date=fields[10],
                        adhar_num=fields[11],
                        adhar_pic=fields[12], 
                        images=[fields[16]],
                        created=fields[14]
                    )
            
            serialize.save()
            
            return Response(data={"success":"added new property"})
        return Response(data={"message":"not valid data","error":serialize.errors},status=status.HTTP_400_BAD_REQUEST)
            

class PropertyUpdateImageApiView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,):
    serializer_class=ImageSerializer
    queryset=Image
    def put(self, request: Request, *args, **kwargs):
        return self.update(request,*args, **kwargs)
    
    def get(self,request:Request,pk=None,*args,**kwargs):
        return self.retrieve(request,pk,*args,**kwargs)
    def delete(self, request: Request,*args, **kwargs):
        return self.destroy(request,*args, **kwargs)
        

class imageaddApiview(generics.GenericAPIView,mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    def post(self, request, pk=None, *args, **kwargs):
        property = PropertyDetail.objects.get(id=pk)

        # converts querydict to original dict
        images = dict((request.data).lists())['property_pic']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(img_name)
            file_serializer = self.serializer_class(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save(property=property)
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)


def modify_input_for_multiple_files(property_pic):
    dict = {}
    dict['property_pic'] = property_pic
    return dict