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

    count = graphene.Int()
    profiles = graphene.List(ProfileType)
    name = graphene.String()
    id = graphene.Int()

    def resolve_profiles(self, args, context, info):
        users = self.user_set.all()
        profiles = [user.profile for user in users]
        return profiles

    def resolve_count(self, args, context, info):
        return sum([x.profile.count for x in self.user_set.all()])

    class Meta:
        model = Group
        only_fields = ('name', 'profiles', 'count', 'id')


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

    group = graphene.Field(GroupType, name=graphene.String())
    groups = graphene.List(GroupType)

    def resolve_groups(self, args, context, info):
        return Group.objects.all()

    def resolve_group(self, args, context, info):
        name = args.get('name')
        try:
            return Group.objects.get(name=name)
        except Group.DoesNotExist:
            return None


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


class AddUserToGroup(graphene.Mutation):
    """Mutation for adding users to a group."""

    class Input:
        uuid = graphene.String()
        group_id = graphene.Int()

    group = graphene.Field(GroupType)

    def mutate(self, args, context, info):
        uuid = args.get('uuid')
        group_id = args.get('group_id')
        group = Group.objects.get(id=group_id)
        profile = Profile.objects.get(uuid=uuid)
        user = profile.user
        user.groups.add(group)
        user.save()
        return group
