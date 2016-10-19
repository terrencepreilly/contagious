""" Defines schema for querying Django models """
import graphene
from graphene_django import DjangoObjectType

from .models import Contact


class ContactType(DjangoObjectType):

    class Meta:
        model = Contact
        only_fields = ('id', 'start', 'end')


class QueryType(graphene.ObjectType):

    name = 'Query'
    description = 'Contacts are contiguous times when two people meet.'

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

schema = graphene.Schema(query=QueryType)
