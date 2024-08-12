from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from server.serializers import ServerSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name='category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter servers by category'
        ),
        OpenApiParameter(
            name='qty',
            type=OpenApiTypes.INT,
            description='Limit the number of server instances returned'
        ),
        OpenApiParameter(
            name='by_user',
            type=OpenApiTypes.BOOL,
            description='Filter servers associated with the authenticated user'
        ),
        OpenApiParameter(
            name='by_server_id',
            type=OpenApiTypes.INT,
            description='Filter servers by a specific server ID'
        ),
        OpenApiParameter(
            name='with_num_members',
            type=OpenApiTypes.BOOL,
            description='Include the number of members in each server'
        ),
    ]
)