from django.urls import path
from . import views
app_name = "articles"
urlpatterns = [
    # 클래스 사용시
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:article_pk>/comments/", views.CommentListAPIView.as_view()),
    path("comments/<int:comment_pk>/", views.CommentDetailAPIView.as_view()),
    # 함수 사용시
    # path("", views.article_list, name="article_list"),
    # path("<int:pk>/", views.article_detail, name="article_detail"),

]
