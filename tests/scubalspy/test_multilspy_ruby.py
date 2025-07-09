"""
This file contains tests for running the Ruby Language Server: solargraph
"""

import unittest
from pathlib import PurePath

import pytest
from scubalspy import LanguageServer
from scubalspy.scubalspy_config import Language
from scubalspy.scubalspy_types import CompletionItemKind, Position

from tests.scubalspy.test_sync_scubalspy_ruby import EXPECTED_RESULT
from tests.test_utils import create_test_context


@pytest.mark.asyncio
async def test_scubalspy_ruby_rubyland():
    """
    Test the working of scubalspy with ruby repository - rubyland
    """
    code_language = Language.RUBY
    params = {
        "code_language": code_language,
        "repo_url": "https://github.com/jrochkind/rubyland/",
        "repo_commit": "c243ee2533a5822f5699a2475e492927ace039c7"
    }
    with create_test_context(params) as context:
        lsp = LanguageServer.create(context.config, context.logger, context.source_directory)

        # All the communication with the language server must be performed inside the context manager
        # The server process is started when the context manager is entered and is terminated when the context manager is exited.
        # The context manager is an asynchronous context manager, so it must be used with async with.
        async with lsp.start_server():
            result = await lsp.request_document_symbols(str(PurePath("app/controllers/application_controller.rb")))

            assert isinstance(result, tuple)
            assert len(result) == 2
            symbol_names = list(map(lambda x: x["name"], result[0]))
            assert symbol_names == ['ApplicationController', 'protected_demo_authentication']

            result = await lsp.request_definition(str(PurePath("app/controllers/feed_controller.rb")), 11, 23)

            feed_path = str(PurePath("app/models/feed.rb"))
            assert isinstance(result, list)
            assert len(result) == 2
            assert feed_path in list(map(lambda x: x["relativePath"], result))

            result = await lsp.request_references(feed_path, 0, 7)

            assert isinstance(result, list)
            assert len(result) == 8

            for item in result:
                del item["uri"]
                del item["absolutePath"]

            case = unittest.TestCase()
            case.assertCountEqual(
                result,
                EXPECTED_RESULT,
            )
