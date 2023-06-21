from django.shortcuts import render
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.views import APIView
from learning.serializers import UserEnrolmentSerilizer
from shared.views import (
    DropdownAPIView,
    PaginatedApiView,
)
from .models import (
    Level,
    Course,
    Lecture,
    UserEnrolment,
    Watchlist
)

# Create your views here.

class LevelView(DropdownAPIView):
    ModelClass = Level
    serializer_fields = ["name", "description", "image", "id"]

class CourseView(DropdownAPIView):
    ModelClass = Course
    serializer_fields = [
        "name", "description", "image", "fees", 
        "video_count", "extra_data", "enrolled_user", 
        "trailer", "level__name", "id"
    ]

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.filter(level__id = request.GET.get("id"))

class LectureView(DropdownAPIView):
    ModelClass = Lecture
    serializer_fields = [
        "id",
        "course",
        "thumbnail",
        "views",
        "description",
        "extra_data"
    ]

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.filter(course__id = request.GET.get("id"))
    

class MyEnrollment(PaginatedApiView):

    ModelClass = UserEnrolment
    ModelSerializerClass = UserEnrolmentSerilizer

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.filter(user_id = request.user.id )
    
    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        course = request.data.get("course", "")
        if course:
            try:
                self.ModelClass.objects.create(
                    user_id = request.user.id,
                    course_id = course
                )
                res_status = HTTP_200_OK
                output_status = True
                message = "Success"
            except Exception as e:
                message = str(e)

        else:
            message = "Please provide course id"
        context = {"status": output_status, "detail": message}
        return Response(context, status=res_status, content_type="application/json")
    



class OpenLecture(APIView):

    
    def get(self, request, *args, **kwargs):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        output_data = {}
        video_id = kwargs.get("video_id")

        obj = Lecture.objects.filter(id = video_id)
        if obj.exists():
            try:
                Watchlist.objects.create(
                    course_id = obj.first().course_id,
                    video_id = video_id
                )
                
            except: ...
            output_data = list(obj.values())
            res_status = HTTP_200_OK
            output_status = True
            message = "Success"
        else:
            message = "Please povide valid Lecture Id"

        context = {"status": output_status, "detail": message, "data": output_data[0]}
        return Response(context, status=res_status, content_type="application/json")

class QuizView(APIView):

    def get(self, request, *args, **kwargs):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        output_data = {}
        video_id = kwargs.get("video_id")

        obj = Watchlist.objects.filter(video_id = video_id)
        if obj.exists():
            #TODO
            # obj.update(completed = True)
            # obj = Q.objects.filter(lecture_id = video_id)
            # if obj.exists():
            #     output_data = list(obj.values())[0]
            res_status = HTTP_200_OK
            output_status = True
            message = "Success"

        else:
            message = "You have not started video yet"
        context = {"status": output_status, "detail": message, "data": output_data}
        return Response(context, status=res_status, content_type="application/json")