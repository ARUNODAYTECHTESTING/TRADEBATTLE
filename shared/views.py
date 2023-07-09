from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.conf import settings


class DropdownAPIView(APIView):
    ModelClass = None
    ModelSerializerClass = None
    serializer_fields = []
    object_name = None
    exempt_cache = False
    post_serializer = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.ModelClass:
            raise ValueError('ModelClass field cannot be None')
        if not (self.ModelSerializerClass or self.serializer_fields):
            raise ValueError(
                'Atleast one of serializer_fields or ModelSerializerClass must be specified')

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.all()

    def get_serializer_class(self, request, *args, **kwargs):
        return self.ModelSerializerClass

    def get_serializer_fields(self, request, *args, **kwargs):
        return self.serializer_fields

    def get_serialized_output(self, request, *args, **kwargs):
        model_obj_list = self.get_queryset(request, *args, **kwargs)
        serializer_fields = self.get_serializer_fields(
            request, *args, **kwargs)
        if serializer_fields:
            try:
                out = list(model_obj_list.values(*serializer_fields))
                return out
            except Exception as e:
                pass
        serializer_class = self.get_serializer_class(request, *args, **kwargs)
        if serializer_class:
            return serializer_class(model_obj_list, many=True, context={'request': request}).data
        return list(model_obj_list.values())

    def update_list_output(self, request, output):
        return output

    def get(self, request, *args, **kwargs):

        output_status = True
        output_detail = "success"
        res_status = status.HTTP_200_OK
        output_data = None
        if output_data is None:
            output_data = self.get_serialized_output(request, *args, **kwargs)

        output = {
            'status': output_status,
            'detail': output_detail,
            'data': output_data
        }
        output = self.update_list_output(request, output)
        return Response(output, status=res_status, content_type="application/json")


class PaginatedApiView(APIView):
    ModelClass = None
    ModelSerializerClass = None
    paginated_by = 100

    def get_queryset(self, request, *args, **kwargs):
        return self.ModelClass.objects.all()

    def get_extra_context(self, request, *args, **kwargs):
        return {}

    def get(self, request, *args, **kwargs):
        output_status = False
        output_detail = "Failed"
        output_data = {}
        res_status = status.HTTP_400_BAD_REQUEST
        end = False
        qs = self.get_queryset(request, *args, **kwargs)
        if qs:
            page = request.GET.get("page", 1)
            try:
                page = int(page)
            except Exception as e:
                page = 1
            qs = qs[self.paginated_by * (page - 1) : self.paginated_by * page]
            if qs.__len__() < self.paginated_by:
                end = True
            output_status = True
            output_detail = "Success"
            res_status = status.HTTP_200_OK

            output_data = self.ModelSerializerClass(
                qs, many=True, context={"request": request}
            ).data

        else:
            output_detail = "No data found"
        context = {
            "status": output_status,
            "detail": output_detail,
            "data": output_data,
            "end": end,
        }
        extra_content = self.get_extra_context(request, *args, **kwargs)
        if extra_content:
            context.update(extra_content)
        return Response(context, status=res_status, content_type="application/json")
