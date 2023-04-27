from rest_framework import serializers
from accounts.serializers import OwnerSerializer
from .models import PropertyDetail,property_to_excel,Image
from rest_framework.request import Request
from accounts.models import User
class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = [
            'id',
            'property_pic'
        ]

class ProperySerializer(serializers.ModelSerializer):
    
    images=ImageSerializer(many=True,read_only=True)
    uploaded_images=serializers.ListField(child=serializers.FileField(allow_empty_file=False,use_url=False),write_only=True)
    class Meta:
        model = PropertyDetail
        fields=["id","property_name","email","tenant_name","address","bhk","age","phone_number","rent","rent_date","adhar_num","adhar_pic","rent_due_date","is_tenant_active","is_paid","images","uploaded_images",'is_property_active']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self,validated_data):
        # url=[]
        
        uploaded_images=validated_data.pop("uploaded_images")
        #user = User.objects.get(**validated_data)
        property=PropertyDetail.objects.create(**validated_data)

        for image in uploaded_images:
            new_image=Image.objects.create(property=property,property_pic=image)
            # url.append(new_image)
        return property
        
class Propertyserializer(serializers.ModelSerializer): 
    class Meta:
        model=PropertyDetail
        exclude="owner",    
    
    

       

        

class CurrentUserPropertySerialzer(serializers.ModelSerializer):
    property = ProperySerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'property']
    


    
class ImportSerializer(serializers.ModelSerializer):
    class Meta:
        model=property_to_excel
        fields="__all__"
