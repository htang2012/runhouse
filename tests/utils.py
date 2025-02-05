import contextlib
import importlib
import uuid
from pathlib import Path

import pytest

from runhouse.globals import rns_client
from runhouse.servers.obj_store import ObjStore, RaySetupOption


def get_ray_servlet_and_obj_store(env_name):
    """Helper method for getting auth servlet and base env servlet"""

    test_obj_store = ObjStore()
    test_obj_store.initialize(env_name, setup_ray=RaySetupOption.TEST_PROCESS)

    servlet = ObjStore.get_env_servlet(
        env_name=env_name,
        create=True,
    )

    return servlet, test_obj_store


def get_random_str(length: int = 8):
    if length > 32:
        raise ValueError("Max length of random string is 32")

    return str(uuid.uuid4())[:length]


@contextlib.contextmanager
def friend_account():
    """Used for the purposes of testing resource sharing among different accounts.
    When inside the context manager, use the test account credentials before reverting back to the original
    account when exiting."""

    local_rh_package_path = Path(
        importlib.util.find_spec("runhouse").origin
    ).parent.parent
    dotenv_path = local_rh_package_path / ".env"
    if not dotenv_path.exists():
        dotenv_path = None  # Default to standard .env file search

    try:
        account = rns_client.load_account_from_env(
            token_env_var="TEST_TOKEN",
            usr_env_var="TEST_USERNAME",
            dotenv_path=dotenv_path,
        )
        if account is None:
            pytest.skip("`TEST_TOKEN` or `TEST_USERNAME` not set, skipping test.")
        yield account

    finally:
        rns_client.load_account_from_file()


@contextlib.contextmanager
def logged_out():
    """Used for the purposes of testing methods as if we're logged out.
    When inside the context manager, token, username, and configs will all be None, as if logged out."""

    rns_client._current_folder = None
    rns_client._configs._simulate_logged_out = True

    yield account

    rns_client._configs._simulate_logged_out = False


@contextlib.contextmanager
def invalid_friend_account():
    """Used for the purposes of testing methods as if we have invalid token.
    When inside the context manager, the friend account role will be assumed, but the token will be set to junk."""

    with friend_account() as friend_account_dict:
        friend_account_dict["token"] = "junk"
        rns_client._configs.token = "junk"

        yield friend_account_dict
