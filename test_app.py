import os
import tempfile

import pytest

from server import app
from models.shared import db

@pytest.fixture
def client():
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
        yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])

def test_empty_db(client):
    rv = client.get("/")
    assert 200 == rv.status_code

def register(client, user_type, name, email, password):
    return client.post("/register", data=dict(
        user_type= user_type,
        name= name,
        email= email,
        password= password,
        verify_password= password
    ), follow_redirects=True)

def login(client, user_type, email, password):
    return client.post("/login", data=dict(
        user_type= user_type,
        email= email,
        password= password
    ), follow_redirects=True)

def logout(client):
    return client.get("/logout", follow_redirects=True)

def test_login_cases(client):
    user_type = "teacher"
    email = "test@test.com"
    password = "password1234"

    rv = register(client, user_type, "Test Teacher", email, password)
    assert 200 == rv.status_code

    rv = logout(client)
    assert 200 == rv.status_code

    rv = login(client, user_type, email, password)
    assert b"Logged in successfully" in rv.data

    rv = logout(client)
    assert 200 == rv.status_code

    rv = login(client, user_type, email + "x", password)
    assert b"No such user" in rv.data

    rv = login(client, user_type, email, password + "x")
    assert b"Incorrect email or password!" in rv.data

def test_create_classroom(client):
    user_type = "teacher"
    email = "test@test.com"
    password = "password1234"

    login(client, user_type, email, password)
    rv = client.post("/classroom/create", data=dict(
        class_name= "DSA",
        class_desc= "Data structures and algorithms"
    ), follow_redirects=True)
    assert b"Classroom created successfully" in rv.data

if __name__ == "__main__":
    test_login_cases(client)
    test_create_classroom(client)