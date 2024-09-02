from rest_framework import serializers
from .models import Article
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("article",)  # article은 읽기 전용으로 부름

    def to_representation(self, instance):  # 보여주는 함수 오버라이딩
        ret = super().to_representation(instance)
        ret.pop('article')  # forms에 except같은 것
        return ret


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(
        source="comments.count", read_only=True)
