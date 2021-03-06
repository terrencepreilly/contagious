"""The schema for profiles."""

from random import Random

from django.contrib.auth.models import Group, User

import graphene
from graphene_django import DjangoObjectType

from .models import Profile


class ProfileType(DjangoObjectType):

    count = graphene.Int()
    status = graphene.String()
    sickdays = graphene.Int()

    class Meta:
        model = Profile
        only_fields = ('uuid', 'count', 'status', 'sickdays')


class UserInputType(graphene.InputObjectType):

    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class GroupType(DjangoObjectType):

    count = graphene.Int()
    profiles = graphene.List(ProfileType)
    name = graphene.String()
    id = graphene.Int()
    size = graphene.Int()
    sick_member_amount = graphene.Int()
    healthy_member_amount = graphene.Int()

    def resolve_profiles(self, args, context, info):
        users = self.user_set.all()
        profiles = [user.profile for user in users]
        return profiles

    def resolve_count(self, args, context, info):
        return sum([x.profile.count for x in self.user_set.all()])

    def resolve_size(self, args, context, info):
        return self.user_set.count()

    def resolve_sick_member_amount(self, args, context, info):
        amount = sum([1 for user in self.user_set.all()
                      if user.profile.sick])
        return amount

    def resolve_healthy_member_amount(self, args, context, info):
        amount = sum([1 for user in self.user_set.all()
                      if user.profile.sick])
        return self.user_set.count() - amount

    class Meta:
        model = Group
        only_fields = ('name', 'profiles', 'count', 'id')


class AdvancedProfileType(DjangoObjectType):
    """ The profile type, which includes displays of groups. """

    count = graphene.Int()
    status = graphene.String()
    sickdays = graphene.Int()
    groups = graphene.List(GroupType)

    def resolve_groups(self, args, context, info):
        return self.user.groups.all()

    class Meta:
        model = Profile
        only_fields = ('uuid', 'count', 'status', 'sickdays', 'groups')


class GroupInputType(graphene.InputObjectType):

    name = graphene.String(required=True)


class ProfileQueryType(object):

    profile = graphene.Field(AdvancedProfileType, uuid=graphene.String())
    profiles = graphene.List(AdvancedProfileType)

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
        user = User.objects.filter(username=username)
        if user.count() > 0:
            return AddProfile(profile=user.first().profile)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            )
        if Random().random() < 0.05:
            user.profile.infect()
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
