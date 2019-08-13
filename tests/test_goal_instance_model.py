import unittest
from app import create_app, db
from api.models import GoalInstance
from api.exceptions import ValidationError


class GoalModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_from_json(self):
        json_goal_instance = {}
        with self.assertRaises(ValidationError):
            GoalInstance.from_json(json_goal_instance)
        json_goal_instance = {"goal_id": ""}
        with self.assertRaises(ValidationError):
            GoalInstance.from_json(json_goal_instance)
        json_goal_instance = {"goal_id": "1"}
        gi = GoalInstance.from_json(json_goal_instance)
        self.assertTrue(isinstance(gi, GoalInstance))

    def test_to_json(self):
        gi = GoalInstance(goal_id="1")
        db.session.add(gi)
        db.session.commit()
        with self.app.test_request_context("/"):
            json_goal_instance = gi.to_json()
        expected_keys = ["id", "goal_id", "timestamp"]
        self.assertEqual(sorted(json_goal_instance.keys()),
                         sorted(expected_keys))

    def test_date_property(self):
        gi = GoalInstance(goal_id="1")
        db.session.add(gi)
        db.session.commit()
        self.assertTrue(isinstance(gi.date, str))
