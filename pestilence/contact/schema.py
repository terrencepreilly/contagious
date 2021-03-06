""" Defines schema for querying Django models """
from django.utils.dateparse import parse_datetime

import graphene
from graphene_django import DjangoObjectType

from .models import Contact
from pest_auth.models import Profile


class ContactType(DjangoObjectType):

    class Meta:
        model = Contact
        only_fields = ('id', 'start', 'end', 'profiles')


class ContactQueryType(object):

    contact = graphene.Field(ContactType, id=graphene.String())
    contacts = graphene.List(ContactType)

    def resolve_contacts(self, args, context, info):
        return Contact.objects.all()

    def resolve_contact(self, args, context, info):
        id = args.get('id')
        try:
            return Contact.objects.get(pk=id)
        except Contact.DoesNotExist:
            return None


class AddContact(graphene.Mutation):
    """Mutation for creating a new Contact."""

    class Input:
        id1 = graphene.String()
        id2 = graphene.String()
        start = graphene.String()
        end = graphene.String()

    contact = graphene.Field(ContactType, id=graphene.String())
    # TODO add error field

    def mutate(self, args, context, info):
        """Create a new Contact

        args:
            id1: The uuid for the first profile in the contact.
            id2: The uuid for the second profile in the contact.
            start: The start time (from the phone's perspective)
                of the contact.
            end: The end time (from the phone's perspective)
                of the contact.
        """
        # TODO add error checking
        start = parse_datetime(args.get('start'))
        end = parse_datetime(args.get('end'))
        contact = Contact(
            start=start,
            end=end,
            )
        profile1 = Profile.objects.get(
            uuid=args.get('id1'))
        profile2 = Profile.objects.get(
            uuid=args.get('id2'))
        contact.save()
        contact.profiles.add(profile1)
        contact.profiles.add(profile2)
        contact.save()
        return AddContact(contact=contact)
