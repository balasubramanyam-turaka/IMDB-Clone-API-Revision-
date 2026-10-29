from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True) 
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ('watchlist',) 

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = '__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'
























# watchlist = serializers.StringRelatedField(many=True) #watchlist is the related_name of the ForeignKey field in the WatchList model. It is used to get the related WatchList objects for a StreamPlatform object. The many=True argument is used because a StreamPlatform can have multiple WatchList objects related to it. The read_only=True argument is used because we don't want to allow the user to create or update WatchList objects through the StreamPlatformSerializer.
# watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
# watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='watchlist-detail')  #view_name is the name of the url pattern for the detail view of the WatchList model.
# watchlist = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='watchlist-detail')  #view_name is the name of the url pattern for the detail view of the WatchList model.










# class MovieSerializer(serializers.ModelSerializer):
#     # len_name = serializers.SerializerMethodField()
    
#     # def get_len_name(self, object):
#     #     return len(object.name)
    
#     class Meta:
#         model = Movie
#         fields = '__all__'
        # fields = ['name', 'description', 'active']
        # exclude = ['id']
        
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and description cannot be the same.")
    #     return data
    
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name must be at least 2 characters long.")
    #     return value




# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name must be at least 2 characters long.")
    
    
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
#     def delete(self, instance):
#         instance.delete()
#         return instance
    
#     #Field level validation
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name must be at least 2 characters long.")
#     #     return value
    
#     #Object level validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and description cannot be the same.")
#         return data