import channels
import channels.auth
from django.urls import path
from framework.schema import MyGraphqlWsConsumer
# from django.core.asgi import get_asgi_application

# from .middleware import i69TokenAuthMiddlewareStack

# application = channels.routing.ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": i69TokenAuthMiddlewareStack(
#         channels.routing.URLRouter([
#             path("ws/graphql", MyGraphqlWsConsumer.as_asgi()),
#         ])
#     ),
# })

application = channels.routing.ProtocolTypeRouter(
    {
        # "http": get_asgi_application(),
        "websocket": channels.auth.AuthMiddlewareStack(
            channels.routing.URLRouter(
                [
                    path("ws/graphql", MyGraphqlWsConsumer.as_asgi()),
                ]
            )
        ),
    }
)
