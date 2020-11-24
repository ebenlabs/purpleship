"""
purplship server accounts module urls
"""
from django.urls import include, path
from django.conf import settings

from purpleserver.client.views import index
from purpleserver.client.views.user import UserAPI
from purpleserver.client.views.token import TokenAPI
from purpleserver.client.views.logs import LogsAPI, LogDetailsAPI, ShipmentsLogsAPI
from purpleserver.client.views.connections import ConnectionList, ConnectionDetails

urlpatterns = [
    path('', index, name='index'),
    path('settings', index, name='settings'),
    path('developers', index, name='developers'),
    path('carrier_connections', index, name='carrier_connections'),
    path('api_logs', index, name='api_logs'),
    path('api_logs/<str:log_id>', index, name='api_logs'),
    path('create/label', index, name='create_label'),

    path('', include('django.contrib.auth.urls')),
    path('', include(settings.CLIENT_REGISTRATION_VIEWS)),
    path('token', TokenAPI.as_view(), name='token'),
    path('user_info', UserAPI.as_view(), name='user_info'),
    path('logs', LogsAPI.as_view(), name='logs'),
    path('logs/<str:log_id>', LogDetailsAPI.as_view(), name='logs'),
    path('shipments', ShipmentsLogsAPI.as_view(), name='shipments_logs'),
    path('connections', ConnectionList.as_view()),
    path('connections/<str:pk>', ConnectionDetails.as_view()),
]
