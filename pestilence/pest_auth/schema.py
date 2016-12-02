"""The schema for profiles."""

from django.contrib.auth.models import Group, User

import graphene
from graphene_django import DjangoObjectType

from .models import Profile


class ProfileType(DjangoObjectType):

    count = graphene.Int()

    class Meta:
        model = Profile
        only_fields = ('uuid', 'count')


class UserInputType(graphene.InputObjectType):

    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class GroupType(DjangoObjectType):

    profiles = graphene.List(ProfileType)

    def resolve_profiles(self, args, context, info):
        users = self.user_set.all()
        profiles = [user.profile for user in users]
        return profiles

    class Meta:
        model = Group
        only_fields = ('name', 'profiles')


class GroupInputType(graphene.InputObjectType):

    name = graphene.String(required=True)


class ProfileQueryType(object):

    profile = graphene.Field(ProfileType, uuid=graphene.String())
    profiles = graphene.List(ProfileType)

    def resolve_profiles(self, args, context, info):
        return Profile.objects.all()

    def resolve_profile(self, args, context, info):
        uuid = args.get('uuid')
        try:
            return Profile.objects.get(uuid=uuid)
        except Profile.DoesNotExist:
            return None


class GroupQueryType(object):

    groups = graphene.List(GroupType)

    def resolve_groups(self, args, context, info):
        return Group.objects.all()


class AddProfile(graphene.Mutation):
    """Mutation for creating a new Contact."""

    class Input:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    profile = graphene.Field(ProfileType)

    def mutate(self, args, context, info):
        username = args.get('username')
        email = args.get('email')
        password = args.get('password')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            )
        return AddProfile(profile=user.profile)


class AddGroup(graphene.Mutation):
    """Mutation for creating a new group, or adding members."""

    class Input:
        name = graphene.String()

    group = graphene.Field(GroupType)

    def mutate(self, args, context, info):
        name = args.get('name')
        group = Group.objects.create(name=name)
        return AddGroup(group=group)
