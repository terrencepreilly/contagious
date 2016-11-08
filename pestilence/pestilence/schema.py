"""Join all of the schemas"""

import graphene
import graph_auth.schema

from contact.schema import (
    ContactQueryType,
    )
from pest_auth.schema import (
    ProfileQueryType,
    )


class QueryType(ContactQueryType,
                ProfileQueryType,
                graph_auth.schema.Query,
                graphene.ObjectType):

    name = 'Query'
    description = 'Queries for pestilence'

    node = graphene.relay.Node.Field()

    # "inherit" class attributes
    # TODO: Is there a better way to do these?
    profiles = ProfileQueryType.profiles

    contact = ContactQueryType.contact
    contacts = ContactQueryType.contacts


schema = graphene.Schema(query=QueryType)
