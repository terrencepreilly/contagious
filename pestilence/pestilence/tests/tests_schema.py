from unittest import skip
from datetime import datetime
import pytz

from django.contrib.auth.models import Group, User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.test import TestCase

from contact.models import Contact
from pest_auth.models import Profile
from pestilence.schema import schema


def convert_time(t: str):
    """Convert a string time (UTC) to UTC."""
    return parse_datetime(t)


def _create_user(number):  # pylint:disable=missing-docstring
    name = 'test{}'.format(number)
    user = User.objects.create_user(
        name,
        name + '@example.com',
        name + 'password',
        )
    return user.profile


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

    def test_query_for_contact_by_profile_uuid(self):
        query = '''
            query {
                profile(uuid: "%(uuid)s") {
                   count
                }
            }
        '''
        profile = _create_user(1)
        query = query % {"uuid": profile.uuid}
        self.contact.profiles.add(profile)
        self.contact.save()
        result = schema.execute(query)
        self.assertFalse(result.invalid, str(result.errors))
        self.assertEqual(result.data['profile']['count'], 1)

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

    @skip('Errors cant be explicitly raised?')
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
        self.profile = self.user.profile

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

    def test_query_get_count(self):
        query = '''
            query {
                profile(uuid: "%(uuid)s") {
                    count
                }
            }
        '''
        contact = Contact(
            start=datetime(2001, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
            end=datetime(2001, 1, 1, 0, 30, 0, tzinfo=pytz.UTC),
            )
        contact.save()
        contact.profiles.add(self.profile)
        query = query % {'uuid': self.profile.uuid}
        result = schema.execute(query)
        self.assertFalse(result.invalid, str(result.errors))

    def test_create_new_profile(self):
        prev_users = User.objects.count()
        prev_profs = Profile.objects.count()
        mutation = '''
            mutation ProfileMutation {
                addProfile(username: "jerry",
                           email: "jerry@aol.com",
                           password: "jerryrocks") {
                    profile {
                        uuid
                    }
               }
            }
        '''
        result = schema.execute(mutation)
        self.assertFalse(result.invalid, str(result.errors))
        self.assertTrue('uuid' in result.data['addProfile']['profile'])
        self.assertTrue(prev_users+1, User.objects.count())
        self.assertTrue(prev_profs+1, Profile.objects.count())

    def test_create_existing_user_returns_profile(self):
        prev_users = User.objects.count()
        prev_profs = Profile.objects.count()
        mutation = '''
            mutation ProfileMutation {
                addProfile(username: "%(username)s",
                           email: "%(email)s",
                           password: "random information") {
                    profile {
                        uuid
                    }
               }
            }
        '''
        mutation = mutation % {
            'username': self.user.username,
            'email': self.user.email,
            }
        result = schema.execute(mutation)
        self.assertFalse(result.invalid, str(result.errors))
        self.assertTrue('uuid' in result.data['addProfile']['profile'])
        self.assertEqual(
            result.data['addProfile']['profile']['uuid'],
            str(self.user.profile.uuid),
            )
        self.assertTrue(prev_users, User.objects.count())
        self.assertTrue(prev_profs, Profile.objects.count())


class GroupSchemaTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@test.com', 'test'
            )
        self.user2 = User.objects.create_user(
            'test2', 'test2@test.com', 'test2'
            )

    def test_create_new_group(self):
        prev_groups = Group.objects.count()
        mutation = '''
            mutation GroupMutation {
                addGroup(name: "mygroup") {
                    group {
                        name
                    }
                }
            }
        '''
        result = schema.execute(mutation)
        self.assertFalse(result.invalid, str(result.errors))
        self.assertEqual(
            prev_groups + 1,
            Group.objects.count(),
            )

    def test_list_all_groups(self):
        group = Group.objects.create(name='testgroup')
        self.user.groups.add(group)
        self.user.save()
        query = '''
            query {
                groups {
                    name
                }
            }
        '''
        result = schema.execute(query)
        self.assertFalse(result.invalid, str(result.errors))

    def test_add_user_to_group(self):
        group = Group.objects.create(name='testgroup')
        mutation = '''
            mutation GroupMutation {
                addUserToGroup(uuid: "%(uuid)s", groupId: %(group_id)s) {
                    group {
                        name
                        profiles {
                            uuid
                        }
                    }
                }
            }
        '''
        mutation = mutation % {
            'uuid': self.user.profile.uuid,
            'group_id': group.id,
            }
        result = schema.execute(mutation)
        self.assertFalse(result.invalid, str(result.errors))
        self.assertEqual(self.user.groups.first(), group)

    def test_group_list_profiles(self):
        group = Group.objects.create(name='testgroup')
        self.user.groups.add(group)
        self.user.save()
        query = '''
            query {
                groups {
                    profiles {
                        uuid
                    }
                }
            }
        '''
        result = schema.execute(query)
        self.assertFalse(result.invalid, result.errors)
        self.assertTrue(len(result.data['groups']), 1)
        self.assertTrue(len(result.data['groups'][0]['profiles']), 1)
        self.assertEqual(result.data['groups'][0]['profiles'][0]['uuid'],
                         str(self.user.profile.uuid))

    def test_can_view_count_of_views_in_group(self):
        group = Group.objects.create(name='testgroup')
        self.user.groups.add(group)
        self.user2.groups.add(group)
        query = '''
            query {
                group(name: "%(name)s") {
                    count
                }
            }
            '''
        query = query % {'name': group.name}
        result = schema.execute(query)
        self.assertFalse(result.invalid, result.errors)
