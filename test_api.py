import os
import unittest
from functools import wraps
from unittest.mock import patch


def mock_decorator(*args, **kwargs):
    """Decorate by doing nothing."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return decorator


patch("api.decorator.requires_auth", mock_decorator).start()


class TestApi(unittest.TestCase):
    os.environ["DB_USERNAME"] = "postgres"
    os.environ["DB_NAME"] = "app"
    os.environ["DB_PASSWORD"] = "1234567890"

    """This class represents the app test case"""
    def setUp(self):
        from app import create_app
        self.app = create_app()
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        self.client = self.app.test_client()

        self._create_actor({"name": "name", "age": 20, "gender": "male"})
        self._create_movie({"title": "the movie title"})

    def tearDown(self):
        self._delete_actor(self.actor.get("id"))
        self._delete_movie(self.movie.get("id"))
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None

    def _create_actor(self, data):
        response = self.client.post("/actors", json=data, follow_redirects=True)
        self.actor = response.get_json()
        self.assertEqual(response.status_code, 200)

    def _create_movie(self, data):
        response = self.client.post("/movies", json=data, follow_redirects=True)
        self.movie = response.get_json()
        self.assertEqual(response.status_code, 200)

    def _delete_actor(self, _id):
        response = self.client.delete(f"/actors/{_id}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def _delete_movie(self, _id):
        response = self.client.delete(f"/movies/{_id}", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_actor(self):
        response = self.client.get("/actors", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [self.actor])

    def test_update_actor(self):
        id = self.actor.get("id")
        response = self.client.patch(f"/actors/{id}", json={"name": "name_updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "name_updated")

    def test_update_actor_fail(self):
        id = "wrong_test_id"
        response = self.client.patch(f"/actors/{id}", json={"name": "name_updated"})
        self.assertEqual(response.status_code, 404)

    def test_get_movie(self):
        response = self.client.get("/movies", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [self.movie])

    def test_add_actor_to_movie(self):
        actor_id = self.actor.get("id")
        movie_id = self.movie.get("id")

        response = self.client.post(f"movies/{movie_id}/actors/{actor_id}",
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("actors"), [self.actor])

    def test_update_movie(self):
        id = self.movie.get("id")
        response = self.client.patch(f"/movies/{id}", json={"title": "Update movie title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["title"], "Update movie title")