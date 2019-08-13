import unittest
from app import create_app, db
from api.models import Goal, GoalInstance
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
        json_goal = {"name": "Goal 1"}
        with self.assertRaises(ValidationError):
            Goal.from_json(json_goal)
        json_goal = {"name": "Goal 1", "target": ""}
        with self.assertRaises(ValidationError):
            Goal.from_json(json_goal)
        json_goal = {"name": "", "target": "10"}
        with self.assertRaises(ValidationError):
            Goal.from_json(json_goal)
        json_goal = {"target": "10"}
        with self.assertRaises(ValidationError):
            Goal.from_json(json_goal)
        json_goal = {"name": "Goal 1", "target": "10"}
        g = Goal.from_json(json_goal)
        self.assertTrue(isinstance(g, Goal))

    def test_to_json(self):
        g = Goal(name="Goal 1", target="10")
        db.session.add(g)
        db.session.commit()
        with self.app.test_request_context("/"):
            json_goal = g.to_json()
        expected_keys = ["id", "name", "target", "timestamp", "instances"]
        self.assertEqual(sorted(json_goal.keys()), sorted(expected_keys))

    def test_instances_property(self):
        g = Goal(name="Goal 1", target="10")
        gi1 = GoalInstance(goal_id=1)
        db.session.add(g)
        db.session.add(gi1)
        db.session.commit()
        self.assertEqual(len(g.instances), 1)
        gi2 = GoalInstance(goal_id=1)
        db.session.add(gi2)
        db.session.commit()
        self.assertEqual(len(g.instances), 2)

    def test_date_property(self):
        g = Goal(name="Goal 1", target="10")
        db.session.add(g)
        db.session.commit()
        self.assertTrue(isinstance(g.date, str))
