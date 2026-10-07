import pytest
from unittest.mock import AsyncMock, MagicMock
from modules.username.github_check import GithubCheck

@pytest.mark.asyncio
async def test_github_user_found():
    module = GithubCheck()
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"public_repos": 12, "html_url": "https://github.com/octocat"}

    module.client = MagicMock()
    module.client.get = AsyncMock(return_value=mock_response)

    result = await module.run("octocat")

    assert result.status == "FOUND"
    assert "Repos: 12" in result.details
    assert result.category == "username"

@pytest.mark.asyncio
async def test_github_user_not_found():
    module = GithubCheck()

    mock_response = MagicMock()
    mock_response.status_code = 404

    module.client = MagicMock()
    module.client.get = AsyncMock(return_value=mock_response)

    result = await module.run("non_existent_user_12345")

    assert result.status == "NOT_FOUND"