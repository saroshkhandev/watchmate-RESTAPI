from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review
#--------------------------------Header Ends-------------------------------------------------#

#--------------------------------Model Serializer--------------------------------------------#
# In this serializer you dont have to pass each element manually like normal serializer
# you just have to pass fields attribute to just give name only of those fields you want
# to serialize with your serializer. Also one another attribute you have to pass is
# model, in which model those you want fields to be imported and then serialized
# fields = "__all__" is used when you want to import each field and serialize
# if you want to import selected fields just pass a tuple or list of those field names.


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList 
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True) #one to many approach
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"

#----------------------------------------------------------------------------------------------
    #Should be above class Meta if applied.
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     lookup_field='id',
    #     many=True,
    #     read_only=True,
    #     view_name='watch-detail'
    # )
#-----------------------------------------------------------------------------------------------#

# class WatchListSerializer(serializers.ModelSerializer):

#     # len_name = serializers.SerializerMethodField()

#     class Meta:
#         model = WatchList
#         # A list or tuple for custom fields will work totally fine
#         # fields = ('id', 'name', 'description', 'active')
#         # if you want to serialize all then
#         fields = "__all__"
#         # To exclude a particular field I can do this too
#         # exclude = ['active']

#     # def get_len_title(self, object):
#     #     return len(object.title)

# for post request from user you have to validate post data manually

    # def validate(self, data):
    #     if data['title'] == data['storyline']:
    #         raise serializers.ValidationError("Name and Description cannot be same")
    #     return data

    # def validate_title(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name too short")
    #     else:
    #         return value

#--------------------------------Normal Serializer-------------------------------------------
# In this serializer you have to manually pass each element manually from model 
# for example id, name, desc etc.
# Also you have to create functions like create update, validate for each response
# of get post put patch etc. too much work to do manually

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)

#         instance.save()
#         return instance

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description cannot be same")
#         return data

#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name too short")
#     #     else:
#     #         return value
