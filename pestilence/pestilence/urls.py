from django.conf.urls import url
from django.contrib import admin

from graphene_django.views import GraphQLView
from jwt_auth.views import obtain_awt_token

from pestilence.schema import schema  # noqa: F401


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
    url(r'^api-token-auth/', obtain_awt_token),
]
