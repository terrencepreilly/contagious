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

    def test_add_contact(self):
        start = timezone.now()
        user1 = User.objects.create_user('test', 'test@test.com', 'test')
        profile1 = user1.profile
        user2 = User.objects.create_user('test2', 'test2@test.com', 'test2')
        profile2 = user2.profile
        mutation = '''
        mutation ContactMutation {
            addContact(
                    id1: "%(id1)s",
                    id2: "%(id2)s",
                    start: "%(start)s",
                    end: "%(end)s") {
                contact {
                    id
                }
            }
        }
        '''
        end = timezone.now()
        mutation = mutation % {
            'id1': profile1.uuid,
            'id2': profile2.uuid,
            'start': start,
            'end': end,
            }
        result = schema.execute(mutation)
        self.assertFalse(
            result.invalid,
            str(result.errors),
            )

    def test_add_contact_with_bad_data_returns_error(self):
        start = timezone.now()
        mutation = '''
        mutation ContactMutation {
            addContact(
                    id1: "invaliduuid",
                    id2: "invaliduuid",
                    start: "%(start)s",
                    end: "%(end)s") {
                contact {
                    id
                }
            }
        }
        '''
        mutation = mutation % {
            'start': start,
            'end': timezone.now(),
            }
        result = schema.execute(mutation)
        self.assertTrue(result.invalid)


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
