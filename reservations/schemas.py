from drf_spectacular.utils import extend_schema, OpenApiResponse
from reservations.serializers import TicketSerializer


create_ticket_schema = extend_schema(
    request=TicketSerializer,
    responses={
        201: TicketSerializer,
        400: OpenApiResponse(description="Bad Request: Invalid data"),
    },
    operation_id="create_ticket",
    description="Create a new ticket for the authenticated user's reservation.",
)

retrieve_ticket_schema = extend_schema(
    responses={
        200: TicketSerializer,
        403: OpenApiResponse(
            description="Forbidden: You do not have permission to view this ticket."
        ),
    },
    operation_id="get_ticket",
    description="Retrieve a specific ticket for the logged-in user. "
                "Only tickets related to the authenticated user are allowed.",
)
