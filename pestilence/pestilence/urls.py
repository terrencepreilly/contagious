from django.conf.urls import url
from django.contrib import admin

from graphene_django.views import GraphQLView
from rest_framework_jwt.views import obtain_jwt_token

from pestilence.schema import schema  # noqa: F401


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^api-token-auth/', obtain_jwt_token),
]
