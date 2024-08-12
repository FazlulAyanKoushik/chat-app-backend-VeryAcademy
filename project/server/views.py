from django.db import models
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from server.models import Server
from server.schema import server_list_docs
from server.serializers import ServerSerializer


# Create your views here.
class ServerViewSet(viewsets.ViewSet):
    """
    Handles API requests for server instances.
    """
    serializer_class = ServerSerializer

    def get_queryset(self):
        queryset = Server.objects.all()
        request = self.request

        # Retrieve query parameters
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Filter by category if provided
        if category:
            queryset = queryset.filter(category__name=category)

        # Limit the queryset by quantity if provided
        if qty and qty.isdigit() and int(qty) > 0:
            queryset = queryset[:int(qty)]

        # Filter by user if by_user is True
        if by_user:
            if request.user.is_authenticated:
                queryset = queryset.filter(members=request.user.id)
            else:
                raise AuthenticationFailed("User is not authenticated")

        # Filter by server ID if provided
        if by_server_id:
            if not request.user.is_authenticated:
                raise AuthenticationFailed("User is not authenticated")
            queryset = queryset.filter(id=by_server_id)
            if not queryset.exists():
                raise Http404("Server not found")

        # Annotate with the number of members if requested
        if with_num_members:
            queryset = queryset.annotate(num_members=models.Count("members"))

        return queryset

    @server_list_docs
    def list(self, request):
        try:
            # Retrieve the filtered and annotated queryset
            queryset = self.get_queryset()

            # Serialize the queryset and return the data in the response
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)

        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Http404 as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            # Retrieve the server instance
            server = Server.objects.get(id=pk)

            # Serialize the server instance and return the data in the response
            serializer = self.serializer_class(server)
            return Response(serializer.data)

        except Server.DoesNotExist:
            return Response({"error": "Server not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
