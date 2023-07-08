from django.urls.conf import path

from .views import (
    LevelView,
    CourseView,
    LectureView,
    MyEnrollment,
    OpenLecture,
    QuizView,
    BookView,
    BookMarkView,
    CategoryView,
    BookMarkListView
)

urlpatterns = [
    path("level/", LevelView.as_view()),
    path("category/", CategoryView.as_view()),
    path("course/", CourseView.as_view()),
    path("lecture/", LectureView.as_view()),
    path("enrollment/", MyEnrollment.as_view()),
    path("open-lecture/<int:video_id>/", OpenLecture.as_view()),
    path("quiz/<int:video_id>/", QuizView.as_view()),
    path("book/<int:video_id>/", BookView.as_view()),
    path("book-mark-list/", BookMarkListView.as_view()),
    path("bookmark/", BookMarkView.as_view()),
]
