from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleDetailSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


# @api_view(["GET", "POST"])
# def article_list(request):
#     if request.method == "GET":
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ArticleSerializer(data=request.data)
#         # return Response(serializer.errors, status=400)을 대신함
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             # 201은 created
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def article_detail(request, pk):
#     if request.method == "GET":
#         article = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         article = get_object_or_404(Article, pk=pk)
#         # 앞에 article을 넣어야 instance처럼 동작
#         serializer = ArticleSerializer(article, data=request.data, partial=True) # partial은 부분 필드만 고치고 싶을때
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#     elif request.method == "DELETE":
#         article = get_object_or_404(Article, pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)  # 204는 삭제


class ArticleListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        # return Response(serializer.errors, status=400)을 대신함
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # 201은 created
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # 자주 쓰는 함수는 요렇게 따로 정의
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        # 앞에 article을 넣어야 instance처럼 동작
        serializer = ArticleDetailSerializer(
            article, data=request.data, partial=True)  # partial은 부분 필드만 고치고 싶을때
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # 204는 삭제


class CommentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serialier = CommentSerializer(comments, many=True)
        return Response(serialier.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            # serializer.data를 빈{}로 보내도 됨
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        data = {"pk": f"{comment_pk} is deleted."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
