from django.shortcuts import render
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView
from learning.serializers import (
    BookmarkSerializer,
    CourseSerializer,
    QuestionSerializer,
    UserEnrolmentSerilizer,
)
from shared.views import (
    DropdownAPIView,
    PaginatedApiView,
)
from .models import (
    Answer,
    Level,
    Course,
    Lecture,
    Pages,
    Question,
    UserEnrolment,
    Watchlist,
    BookMark,
    Category,
)
from django.db.models import F

# Create your views here.


class LevelView(DropdownAPIView):
    ModelClass = Level
    serializer_fields = ["name", "description", "image", "id"]


class CategoryView(DropdownAPIView):
    ModelClass = Category
    serializer_fields = ["name", "id"]


class CourseView(DropdownAPIView):
    ModelClass = Course
    ModelSerializerClass = CourseSerializer

    def update_list_output(self, request, output):
        completed_course = UserEnrolment.objects.filter(user_id = request.user.id, completed = True)
        output["completed"] = completed_course.count()
        return output

    def get_queryset(self, request, *args, **kwargs):
        category = request.GET.get("category")
        if category:
            return self.ModelClass.objects.filter(category_id=category)
        return self.ModelClass.objects.all().order_by("level_id")


class LectureView(DropdownAPIView):
    ModelClass = Lecture
    serializer_fields = [
        "id",
        "course",
        "thumbnail",
        "views",
        "description",
        "extra_data",
    ]

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.filter(course__id=request.GET.get("id"))


class MyEnrollment(PaginatedApiView):
    ModelClass = UserEnrolment
    ModelSerializerClass = UserEnrolmentSerilizer

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.filter(user_id=request.user.id)

    def post(self, request):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        course = request.data.get("course", "")
        if course:
            try:
                self.ModelClass.objects.create(
                    user_id=request.user.id, course_id=course
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

        obj = Lecture.objects.filter(id=video_id)
        if obj.exists():
            try:
                Watchlist.objects.create(
                    course_id=obj.first().course_id, video_id=video_id
                )

            except:
                ...
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
        output_data = []
        video_id = kwargs.get("video_id")

        obj = Watchlist.objects.filter(video_id=video_id)
        if obj.exists():
            ques = Question.objects.filter(lecture_id=video_id)
            if ques.exists():
                obj.update(quiz_atempt=F("quiz_atempt") + 1, completed=True)
                output_data = QuestionSerializer(ques, many=True).data
                res_status = HTTP_200_OK
                output_status = True
                message = "Success"
            else:
                message = "No Question Exist"
        else:
            message = "You have not started video yet"
        context = {"status": output_status, "detail": message, "data": output_data}
        return Response(context, status=res_status, content_type="application/json")

    def post(self, request, *args, **kwargs):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        output_data = {}
        answer_list = request.data.get("answer", [])
        video_id = kwargs.get("video_id")
        obj = Watchlist.objects.filter(video_id=video_id)
        if obj.exists():
            total_count = Question.objects.filter(lecture_id=video_id).count()
            if answer_list:
                obj = obj.first()
                if obj.quiz_atempt < 3:
                    correct_obj = Answer.objects.filter(
                        correct=True, id__in=answer_list, question__lecture_id=video_id
                    )
                    correct_count = correct_obj.count()

                    if correct_count > 5:
                        request.user.experience_point += 25
                        request.user.save()
                    res_status = HTTP_200_OK
                    output_status = True
                    message = "Success"
                    output_data = {
                        "correct": correct_count,
                        "total": total_count,
                        "points": 25,
                    }
                else:
                    message = "You have reached Maximum Attempt"
            else:
                res_status = HTTP_200_OK
                output_status = True
                message = "Success"
                output_data = {"correct": 0, "total": total_count}
        else:
            message = "You have not started video yet"

        context = {"status": output_status, "detail": message, "data": output_data}
        return Response(context, status=res_status, content_type="application/json")


class BookView(APIView):
    def get(self, request, *args, **kwargs):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        output_data = {}
        video_id = kwargs.get("video_id")
        page = request.GET.get("page")
        obj = Watchlist.objects.filter(video_id=video_id)
        if obj.exists():
            page_obj = Pages.objects.filter(lecture_id=video_id)
            if page_obj.exists():
                total_page = page_obj.count()
                try:
                    page = int(page)
                except Exception as e:
                    page = 0
                if page:
                    page_obj = page_obj.filter(page_no=page)
                    if page_obj.exists():
                        output_data = page_obj.values(
                            "description", "id", "page_no"
                        ).first()
                        output_data.update(
                            {
                                "total_page": total_page,
                                "bookmark": BookMark.objects.filter(
                                    user_id=request.user.id, page_id=output_data["id"]
                                ).exists(),
                            }
                        )
                        res_status = HTTP_200_OK
                        output_status = True
                        message = "Success"
                    else:
                        message = "Invalid Page number"
                else:
                    page = obj.first().book_page
                    if total_page > page:
                        page_obj = page_obj.filter(page_no=page + 1)
                        if page_obj.exists():
                            output_data = page_obj.values(
                                "description", "id", "page_no"
                            ).first()
                            output_data.update(
                                {
                                    "total_page": total_page,
                                    "bookmark": BookMark.objects.filter(
                                        user_id=request.user.id,
                                        page_id=output_data["id"],
                                    ).exists(),
                                }
                            )
                            res_status = HTTP_200_OK
                            output_status = True
                            message = "Success"
                            obj.update(book_page=F("book_page") + 1)
                        else:
                            message = "Page not found"
                    else:
                        message = "Book is completed"
            else:
                message = "No book available for this lecture"
        else:
            message = "You have not started video yet"
        context = {"status": output_status, "detail": message, "data": output_data}
        return Response(context, status=res_status, content_type="application/json")


class BookMarkListView(PaginatedApiView):
    ModelClass = BookMark
    ModelSerializerClass = BookmarkSerializer

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.filter(user_id=request.user.id).distinct(
            "page__lecture__course"
        )


class BookMarkView(PaginatedApiView):
    ModelClass = BookMark
    ModelSerializerClass = BookmarkSerializer

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.filter(user_id=request.user.id)

    def post(self, request, *args, **kwargs):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        page = request.data.get("page")
        try:
            self.ModelClass.objects.create(user_id=request.user.id, page_id=page)
            res_status = HTTP_200_OK
            output_status = True
            message = "Success"
        except Exception as e:
            message = str(e)
        context = {"status": output_status, "detail": message}
        return Response(context, status=res_status, content_type="application/json")

    def delete(self, request, *args, **kwargs):
        res_status = HTTP_400_BAD_REQUEST
        output_status = False
        message = "failed"
        page_id = request.data.get("page")
        obj = self.ModelClass.objects.filter(user_id=request.user.id, page_id=page_id)
        if obj.exists():
            obj.delete()
            res_status = HTTP_200_OK
            output_status = True
            message = "Success"
        else:
            message = "No bookmark found"
        context = {"status": output_status, "detail": message}
        return Response(context, status=res_status, content_type="application/json")
