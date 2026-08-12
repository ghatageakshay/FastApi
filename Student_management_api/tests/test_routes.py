from app.main import app


def test_student_post_route_is_registered():
    paths = [route.path for route in app.routes]
    assert "/student" in paths
