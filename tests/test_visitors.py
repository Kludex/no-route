import textwrap

import libcst as cst
import pytest
from libcst.codemod import CodemodContext

from no_route import RouteDecoratorCommand


@pytest.mark.parametrize(
    "input,expected",
    (
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()

            @app.route("/", methods=["GET"])
            def home():
                ...
            """
            ),
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()

            @app.get("/")
            def home():
                ...
            """
            ),
            id="fastapi-app",
        ),
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()

            @app.route("/", methods=["GET"])
            async def home():
                ...
            """
            ),
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()

            @app.get("/")
            async def home():
                ...
            """
            ),
            id="fastapi-async",
        ),
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import APIRouter

            router = APIRouter()

            @router.route("/", methods=["GET"])
            def home():
                ...
            """
            ),
            textwrap.dedent(
                """
            from fastapi import APIRouter

            router = APIRouter()

            @router.get("/")
            def home():
                ...
            """
            ),
            id="fastapi-router",
        ),
        pytest.param(
            textwrap.dedent(
                """
            from flask import Flask

            app = Flask(__name__)

            @app.route("/", methods=["GET"])
            def home():
                ...
            """
            ),
            textwrap.dedent(
                """
            from flask import Flask

            app = Flask(__name__)

            @app.get("/")
            def home():
                ...
            """
            ),
            id="flask-app",
        ),
        pytest.param(
            textwrap.dedent(
                """
            from flask import Blueprint

            router = Blueprint("app", __name__)

            @router.route("/", methods=["GET"])
            def home():
                ...
            """
            ),
            textwrap.dedent(
                """
            from flask import Blueprint

            router = Blueprint("app", __name__)

            @router.get("/")
            def home():
                ...
            """
            ),
            id="flask-blueprint",
        ),
        pytest.param(
            textwrap.dedent(
                """
            router = Potato()

            @router.route("/", methods=["GET"])
            def home():
                ...
            """
            ),
            textwrap.dedent(
                """
            router = Potato()

            @router.route("/", methods=["GET"])
            def home():
                ...
            """
            ),
            id="fake-route",
            marks=pytest.mark.skip(
                "Only FastAPI, Flask, flask.Blueprint and fastapi.APIRouter"
                "should be supported."
            ),
        ),
        pytest.param(
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()

            @app.route("/", methods=["GET", "POST"])
            async def home(request: Request):
                if request.method == "GET":
                    print("This is a GET!")
                else:
                    print("This is a POST!")
            """
            ),
            textwrap.dedent(
                """
            from fastapi import FastAPI

            app = FastAPI()

            @app.get("/")
            async def get_home(request: Request):
                print("This is a GET!")

            @app.post("/")
            async def post_home(request: Request):
                print("This is a POST!")
            """
            ),
            id="multiple-methods",
            marks=pytest.mark.skip("Duplicate of methods are not supported yet."),
        ),
    ),
)
def test_transformer(input: str, expected: str) -> None:
    source_tree = cst.parse_module(input)
    transformer = RouteDecoratorCommand(CodemodContext())
    modified_tree = source_tree.visit(transformer)
    assert modified_tree.code == expected
