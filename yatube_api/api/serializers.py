from rest_framework import serializers

from posts.models import Comment, Post, Group, Follow, User


class FollowingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False,
                                        required=False,
                                        slug_field='username',
                                        queryset=User.objects.all(),
                                        )
    following = serializers.SlugRelatedField(many=False,
                                             read_only=False,
                                             required=True,
                                             slug_field='username',
                                             queryset=User.objects.all(),
                                             )

    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['user']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False,
                                          read_only=True,
                                          required=False,
                                          slug_field='username',
                                          )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post
