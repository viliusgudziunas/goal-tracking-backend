import unittest
from run import create_app, db
from api.models import User, Goal


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password="cat")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password="cat")
        self.assertTrue(u.verify_password("cat"))
        self.assertFalse(u.verify_password("dog"))

    def test_password_salts_are_random(self):
        u = User(password="cat")
        u2 = User(password="cat")
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_to_json(self):
        u = User(email="john@example.com", password="cat")
        db.session.add(u)
        db.session.commit()
        with self.app.test_request_context("/"):
            json_user = u.to_json()
        expected_keys = ["goals"]
        self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))

    def test_goals_property(self):
        u = User(email="john@example.com", password="cat")
        g1 = Goal(author_id=1, name="Goal 1")
        db.session.add(u)
        db.session.add(g1)
        db.session.commit()
        self.assertEqual(len(u.goals), 1)
        g2 = Goal(author_id=1, name="Goal 2")
        db.session.add(g2)
        db.session.commit()
        self.assertEqual(len(u.goals), 2)

    def test_goals_to_json(self):
        u = User(email="john@example.com", password="cat")
        g1 = Goal(author_id=1, name="Goal 1")
        g2 = Goal(author_id=1, name="Goal 2")
        db.session.add(u)
        db.session.add(g1)
        db.session.add(g2)
        db.session.commit()
        expected_keys = ["id", "name", "target", "timestamp", "instances"]
        for json_goal in u.goals_to_json():
            self.assertEqual(sorted(json_goal.keys()), sorted(expected_keys))
