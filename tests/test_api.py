import unittest
import json
from app import create_app, db
from api.models import User, Goal, GoalInstance


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        return {
            "Content-Type": "application/json"
        }

    def test_validation_error(self):
        response = self.client.post(
            "/goals/new-goal",
            headers=self.get_api_headers(),
            data=json.dumps({"body": ""})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["error"], "bad request")

    def test_404(self):
        response = self.client.get(
            "/wrong/url",
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["error"], "not found")

    #
    # User
    #
    def test_get_user(self):
        u = User(email="john@example.com", password="cat")
        db.session.add(u)
        db.session.commit()
        # Request for a user id that does not exist
        response = self.client.get(
            "/users/2",
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 404)

        # Request for a valid user id with no goals
        response = self.client.get(
            "/users/1",
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(json_response), 0)

        g1 = Goal(author_id=1, name="Goal 1")
        g2 = Goal(author_id=1, name="Goal 2")
        db.session.add(g1)
        db.session.add(g2)
        db.session.commit()
        # Request for a valid user id with two goals
        response = self.client.get(
            "/users/1",
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(json_response), 2)
        expected_keys = ["id", "name", "target", "timestamp", "instances"]
        for json_goal in json_response:
            self.assertEqual(sorted(json_goal.keys()), sorted(expected_keys))

        g3 = Goal(author_id=2, name="Goal 3")
        db.session.add(g3)
        db.session.commit()
        # The endpoint doesn't return goals that belong to other users
        response = self.client.get(
            "/users/1",
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(json_response), 2)
        for json_goal in json_response:
            self.assertTrue(json_goal["name"] != "Goal 3")

    #
    # Goal
    #
    def test_goal(self):
        u = User(email="john@example.com", password="cat")
        db.session.add(u)
        db.session.commit()
        # Submit a goal that lacks information
        response = self.client.post(
            "/goals/new-goal",
            headers=self.get_api_headers(),
            data=json.dumps({})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["message"], "Goal does not have a name")

        response = self.client.post(
            "/goals/new-goal",
            headers=self.get_api_headers(),
            data=json.dumps({"name": ""})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["message"], "Goal does not have a name")

        response = self.client.post(
            "/goals/new-goal",
            headers=self.get_api_headers(),
            data=json.dumps({"target": ""})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["message"], "Goal does not have a name")

        response = self.client.post(
            "/goals/new-goal",
            headers=self.get_api_headers(),
            data=json.dumps({"name": "Goal 1"})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["message"],
                         "Goal does not have a target")

        response = self.client.post(
            "/goals/new-goal",
            headers=self.get_api_headers(),
            data=json.dumps({"name": "Goal 1", "target": ""})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["message"],
                         "Goal does not have a target")

        # Successful goal submission
        response = self.client.post(
            "/goals/new-goal",
            headers=self.get_api_headers(),
            data=json.dumps({"name": "Goal 1", "target": "10"})
        )
        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.get_data(as_text=True))
        expected_keys = ["id", "name", "target", "timestamp", "instances"]
        self.assertEqual(sorted(json_response.keys()), sorted(expected_keys))

        # Unsuccessful goal deletion
        response = self.client.post(
            "/goals/delete-goal/2",
            headers=self.get_api_headers()
        )
        self.assertEqual(response.status_code, 404)

        gi = GoalInstance(goal_id=1)
        db.session.add(gi)
        db.session.commit()
        # Successful goal deletion
        self.assertEqual(len(GoalInstance.query.all()), 1)
        # Currently broken while login functionality is being implemented
        # response = self.client.post(
        #     "/goals/delete-goal/1",
        #     headers=self.get_api_headers()
        # )
        # self.assertEqual(response.status_code, 200)
        # print(Goal.query.filter_by(id=1).first())
        # self.assertEqual(len(GoalInstance.query.all()), 0)

        g = Goal(name="Goal 1", target="10")
        db.session.add(g)
        db.session.commit()
        # Unsuccessful goal target change
        # Currently broken while login functionality is being implemented
        # response = self.client.post(
        #     "/goals/change-goal-target/1",
        #     headers=self.get_api_headers(),
        #     data=json.dumps({})
        # )
        # self.assertEqual(response.status_code, 404)

    def test_goal_instance(self):
        g = Goal(id=1, name="Goal 1")
        db.session.add(g)
        db.session.commit()
        # Unsuccessful goal instance creation
        response = self.client.post(
            "/goals/new-goal-instance",
            headers=self.get_api_headers(),
            data=json.dumps({})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["message"],
                         "Goal instance does not have a goal ID")

        response = self.client.post(
            "/goals/new-goal-instance",
            headers=self.get_api_headers(),
            data=json.dumps({"goal_id": ""})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["message"],
                         "Goal instance does not have a goal ID")

        response = self.client.post(
            "/goals/new-goal-instance",
            headers=self.get_api_headers(),
            data=json.dumps({"goal_id": "1"})
        )
        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.get_data(as_text=True))
        expected_keys = ["id", "name", "target", "timestamp", "instances"]
        self.assertEqual(sorted(json_response.keys()), sorted(expected_keys))
