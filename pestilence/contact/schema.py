""" Defines schema for querying Django models """
import graphene
from graphene_django import DjangoObjectType

from .models import Contact


class ContactType(DjangoObjectType):

    class Meta:
        model = Contact


class Query(graphene.ObjectType):

    contacts = graphene.List(ContactType)

    @graphene.resolve_only_args
    def resolve_contacts(self, **kwargs):
        return Contact.objects.all()


schema = graphene.Schema(query=Query)
