"""Join all of the schemas"""

import graphene

from contact.schema import QueryType as contact_query
from pest_auth.schema import QueryType as profile_query

schema = graphene.Schema(query=contact_query)
profile_schema = graphene.Schema(query=profile_query)
