from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import AuthOrOwner, ReadOrOwner
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .serializers import FollowingSerializer
from posts.models import Post, Group, Comment, Follow


class FollowViewSet(viewsets.ModelViewSet):
    """ViewSet for Follow model.

    Create - reassembled because we need 'user' in response.
    get_queryset - reassembled because when request get
    we need only following of request.user.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = [AuthOrOwner]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        # По умолчанию, если переоперделить perform_create,
        # то в ответе не возвращается user на что жалуется pytest.
        data = serializer.validated_data
        data['user'] = self.request.user

        if (self.request.user.follower.filter(
                following=serializer.validated_data['following']).exists()
                or
                self.request.user == serializer.validated_data['following']):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_queryset(self):
        return self.request.user.follower.all()


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model.

    Create - reassembled because we get author of post from request data
    and user shouldn't send this attribute.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ReadOrOwner]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Read_only view set for Group model."""
    permission_classes = [ReadOrOwner]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model.

    get_queryset - reassembled because we use only specific comments
    related to some post.
    Create - reassembled because we get author of comment from request data
    and user shouldn't send this attribute.
    """
    permission_classes = [ReadOrOwner]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)
