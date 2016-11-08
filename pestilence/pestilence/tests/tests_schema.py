from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.test import TestCase

from contact.models import Contact
from pest_auth.models import Profile
from pestilence.schema import schema


def convert_time(t: str):
    """Convert a string time (UTC) to UTC."""
    return parse_datetime(t)


class ContactSchemaTestCase(TestCase):

    def setUp(self):
        self.start = timezone.now()
        self.end = timezone.now()
        self.contact = Contact.objects.create(
            start=self.start,
            end=self.end,
            )

    def test_query_schema(self):
        query = '''
            query {
                contacts {
                    start
                    end
                }
            }
        '''
        result = schema.execute(query)
        self.assertFalse(result.invalid)
        start_time = result.data['contacts'][0]['start']
        start_time = convert_time(start_time)
        self.assertEqual(start_time, self.start)
        end_time = result.data['contacts'][0]['end']
        end_time = convert_time(end_time)
        self.assertEqual(end_time, self.end)

    def test_query_for_specific_contact(self):
        query = '''
            query {
                contact(id: "%(id)s") {
                    id
                    start
                    end
                }
            }
        '''
        query = query % {"id": self.contact.id}
        result = schema.execute(query)
        self.assertFalse(result.invalid)
        end_time = result.data['contact']['end']
        end_time = convert_time(end_time)
        self.assertEqual(end_time, self.end)


class ProfileSchemaTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
        self.profile = Profile(
            user=self.user,
            )

    def test_query_list_uuids(self):
        query = '''
            query {
                profiles {
                    uuid
                }
            }
        '''
        result = schema.execute(query)
        self.assertFalse(result.invalid, str(result.errors))
