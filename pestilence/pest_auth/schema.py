"""The schema for profiles."""

import graphene
from graphene_django import DjangoObjectType

from .models import Profile


class ProfileType(DjangoObjectType):

    class Meta:
        model = Profile
        only_fields = ('uuid',)


class QueryType(graphene.ObjectType):

    name = 'Query'
    description = 'Profiles are the front-facing part of a user.'

    profiles = graphene.List(ProfileType)

    def resolve_profiles(self, args, context, info):
        return Profile.objects.all()
