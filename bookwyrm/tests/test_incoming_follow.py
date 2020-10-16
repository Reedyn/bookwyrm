import json
from django.test import TestCase

from bookwyrm import models, incoming


class Follow(TestCase):
    ''' not too much going on in the books model but here we are '''
    def setUp(self):
        self.remote_user = models.User.objects.create_user(
            'rat', 'rat@rat.com', 'ratword',
            local=False,
            remote_id='https://example.com/users/rat',
            inbox='https://example.com/users/rat/inbox',
            outbox='https://example.com/users/rat/outbox',
        )
        self.local_user = models.User.objects.create_user(
            'mouse', 'mouse@mouse.com', 'mouseword')
        self.local_user.remote_id = 'http://local.com/user/mouse'
        self.local_user.save()


    def test_handle_follow(self):
        activity = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": "https://example.com/users/rat/follows/123",
            "type": "Follow",
            "actor": "https://example.com/users/rat",
            "object": "http://local.com/user/mouse"
        }

        incoming.handle_follow(activity)

        # notification created
        notification = models.Notification.objects.get()
        self.assertEqual(notification.user, self.local_user)
        self.assertEqual(notification.notification_type, 'FOLLOW')

        # the request should have been deleted
        requests = models.UserFollowRequest.objects.all()
        self.assertEqual(list(requests), [])

        # the follow relationship should exist
        follow = models.UserFollows.objects.get(user_object=self.local_user)
        self.assertEqual(follow.user_subject, self.remote_user)

        # an Accept should be sent out
