"""Join all of the schemas"""

import graphene

from contact.schema import (
    ContactQueryType,
    AddContact,
    )
from pest_auth.schema import (
    ProfileQueryType,
    )


class QueryType(ContactQueryType,
                ProfileQueryType,
                graphene.ObjectType):

    name = 'Query'
    description = 'Queries for pestilence'

    node = graphene.relay.Node.Field()

    # "inherit" class attributes
    # TODO: Is there a better way to do these?
    profiles = ProfileQueryType.profiles

    contact = ContactQueryType.contact
    contacts = ContactQueryType.contacts


class ContactMutation(graphene.ObjectType):
    add_contact = AddContact.Field()


schema = graphene.Schema(
    query=QueryType,
    mutation=ContactMutation,
    )
