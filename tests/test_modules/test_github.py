import pytest
from unittest.mock import AsyncMock, MagicMock
from modules.username.github_check import GitHubCheck

@pytest.mark.asyncio
async def test_github_user_found():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"public_repos": 12, "html_url": "https://github.com/octocat"}
    mock_client.get = AsyncMock(return_value=mock_response)

    # Passa o mock_client no construtor
    module = GitHubCheck(http_client=mock_client)

    result = await module.run("octocat")

    assert result.status == "FOUND"
    assert "Repos: 12" in result.details
    assert result.category == "username"

@pytest.mark.asyncio
async def test_github_user_not_found():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.get = AsyncMock(return_value=mock_response)

    # Passa o mock_client no construtor
    module = GitHubCheck(http_client=mock_client)

    result = await module.run("non_existent_user_12345")

    assert result.status == "NOT_FOUND"