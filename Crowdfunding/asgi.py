
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Crowdfunding.settings')

application = get_asgi_application()



# import os

# from django.core.asgi import get_asgi_application

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter

# import room.routing 

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Crowdfunding.settings')

# application = ProtocolTypeRouter({
#     "https":get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             room.routing.websocket_urlpatterns
#         )
#     )
# })