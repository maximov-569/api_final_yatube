from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins

from .permissions import AuthOrOwner, ReadOrOwner
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .serializers import FollowingSerializer
from posts.models import Post, Group, Comment, Follow


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet for Follow model.

    perform_create - reassembled because
    user cannot make follow for other users.
    get_queryset - reassembled because when request get
    we need only following of request.user.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = [AuthOrOwner]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    # Можно не переопределять метод,
    # так как по умолчанию поле юзер поступает из сериализатора,
    # но я не знаю как лучше
    # по этому оставил это здесь как дополнитульную меру осторожности.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
