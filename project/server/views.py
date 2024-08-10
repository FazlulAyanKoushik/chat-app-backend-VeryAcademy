from django.db import models

from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from server.models import Server
from server.serializers import ServerSerializer


# Create your views here.
class ServerViewSet(viewsets.ViewSet):
    """
    Handles API requests for server instances.
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='category',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter servers by category'
            ),
            OpenApiParameter(
                name='qty',
                type=int
            ),
            OpenApiParameter(
                name='by_user',
                type=bool,
            ),
            OpenApiParameter(
                name='by_server_id',
                type=int,
            ),
            OpenApiParameter(
                name='with_num_members',
                type=bool,
            ),
        ]
    )
    def list(self, request):
        try:
            category = request.query_params.get("category")
            qty = request.query_params.get("qty")
            # Check if the request is to filter servers by user, default to False if not provided
            by_user = request.query_params.get("by_user") == "true"
            by_server_id = request.query_params.get("by_server_id")
            with_num_members = request.query_params.get("with_num_members") == "true"

            if by_user and by_server_id and not request.user.is_authenticated:
                raise AuthenticationFailed()

            if category:
                self.queryset = self.queryset.filter(category__name=category)

            if qty and qty.isdigit() and int(qty) > 0:
                # Limit the queryset to the specified positive quantity
                self.queryset = self.queryset[:int(qty)]

            if by_user:
                # Filter the queryset by the user
                user_id = request.user.id
                self.queryset = self.queryset.filter(members=user_id)

            if by_server_id:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    return Response({"error": "Server not found"}, status=status.HTTP_404_NOT_FOUND)

            if with_num_members:
                # Annotate the queryset with the number of members in each server
                self.queryset = self.queryset.annotate(num_members=models.Count("members"))

            serializer = self.serializer_class(self.queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        server = self.queryset.get(pk=pk)
        serializer = self.serializer_class(server)
        return Response(serializer.data)
