from django.conf.urls import url
from django.contrib import admin

from graphene_django.views import GraphQLView

from pestilence.schema import schema  # noqa: F401


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
]
