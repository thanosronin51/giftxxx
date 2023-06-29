from django.urls import path, include 
from .views import QuizListView, CategoriesListView,\
    ViewQuizListByCategory, QuizUserProgressView, QuizMarkingList,\
    QuizMarkingDetail, QuizDetailView, QuizTake

urlpatterns = [

    path('quizzes/', QuizListView.as_view(), name='quiz_index'),
    path('category/', CategoriesListView.as_view(), name='quiz_category_list_all'),
    path('category/<slug:category_name>/', ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),
    path('progress/', QuizUserProgressView.as_view(), name='quiz_progress'),
    path('marking/', QuizMarkingList.as_view(), name='quiz_marking'),
    path('marking/<int:pk>/', QuizMarkingDetail.as_view(), name='quiz_marking_detail'),
    path('<slug:slug>/', QuizDetailView.as_view(), name='quiz_start_page'),
    path('<slug:quiz_name>/take/', QuizTake.as_view(), name='quiz_question'),
]
