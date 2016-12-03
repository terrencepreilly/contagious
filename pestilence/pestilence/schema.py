"""Join all of the schemas"""

import graphene

from contact.schema import (
    ContactQueryType,
    AddContact,
    )
from pest_auth.schema import (
    ProfileQueryType,
    GroupQueryType,
    AddGroup,
    AddProfile,
    AddUserToGroup,
    )


class QueryType(ContactQueryType,
                ProfileQueryType,
                GroupQueryType,
                graphene.ObjectType):

    name = 'Query'
    description = 'Queries for pestilence'

    node = graphene.relay.Node.Field()

    # "inherit" class attributes
    # TODO: Is there a better way to do these?
    profile = ProfileQueryType.profile
    profiles = ProfileQueryType.profiles

    contact = ContactQueryType.contact
    contacts = ContactQueryType.contacts

    groups = GroupQueryType.groups


class Mutation(graphene.ObjectType):
    add_contact = AddContact.Field()
    add_profile = AddProfile.Field()
    add_group = AddGroup.Field()
    add_user_to_group = AddUserToGroup.Field()


schema = graphene.Schema(
    query=QueryType,
    mutation=Mutation,
    )
