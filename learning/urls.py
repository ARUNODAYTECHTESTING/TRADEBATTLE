from django.urls.conf import path

from .views import (
    LevelView,
    CourseView,
    LectureView,
    MyEnrollment,
    OpenLecture,
    QuizView
)

urlpatterns = [
    path("level/", LevelView.as_view()),
    path("course/", CourseView.as_view()),
    path("lecture/", LectureView.as_view()),
    path("enrollment/", MyEnrollment.as_view()),
    path("open-lecture/<video_id>/", OpenLecture.as_view()),
    path("quiz/<video_id>/", QuizView.as_view()),
]