
from unittest.mock import MagicMock, patch

from src.rewriter import rewrite_query


def test_empty_query():
    assert rewrite_query("") == ""


def test_rewriter_without_api_key():
    with patch.dict("os.environ", {"OPENAI_API_KEY": ""}):
        result = rewrite_query("What is Kubernetes?")

    assert result == "What is Kubernetes?"


def test_conversational_pronoun_resolution():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = (
        "What are the system requirements for Kubernetes Worker Nodes?"
    )

    with patch("src.rewriter.OpenAI") as mock_client:
        mock_client.return_value.chat.completions.create.return_value = (
            mock_response
        )

        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "test-key"},
        ):
            result = rewrite_query(
                "What are its system requirements?",
                "We were discussing Kubernetes Worker Nodes.",
            )

    assert "Kubernetes Worker Nodes" in result
