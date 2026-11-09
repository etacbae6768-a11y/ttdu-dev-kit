from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hwp_markdown_result import HwpMarkdownResult
from ...models.hwp_to_markdown_files_body import HwpToMarkdownFilesBody
from ...models.hwp_to_markdown_json_body import HwpToMarkdownJsonBody
from ...models.problem import Problem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: HwpToMarkdownFilesBody | HwpToMarkdownJsonBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/hwp/markdown",
    }

    if isinstance(body, HwpToMarkdownFilesBody):
        _kwargs["files"] = body.to_multipart()

    if isinstance(body, HwpToMarkdownJsonBody):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> HwpMarkdownResult | Problem | None:
    if response.status_code == 200:
        response_200 = HwpMarkdownResult.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Problem.from_dict(response.json())

        return response_400

    if response.status_code == 413:
        response_413 = Problem.from_dict(response.json())

        return response_413

    if response.status_code == 422:
        response_422 = Problem.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = Problem.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[HwpMarkdownResult | Problem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToMarkdownFilesBody | HwpToMarkdownJsonBody | Unset = UNSET,
) -> Response[HwpMarkdownResult | Problem]:
    """HWP/HWPX to Markdown

    Args:
        body (HwpToMarkdownFilesBody):
        body (HwpToMarkdownJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HwpMarkdownResult | Problem]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToMarkdownFilesBody | HwpToMarkdownJsonBody | Unset = UNSET,
) -> HwpMarkdownResult | Problem | None:
    """HWP/HWPX to Markdown

    Args:
        body (HwpToMarkdownFilesBody):
        body (HwpToMarkdownJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HwpMarkdownResult | Problem
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToMarkdownFilesBody | HwpToMarkdownJsonBody | Unset = UNSET,
) -> Response[HwpMarkdownResult | Problem]:
    """HWP/HWPX to Markdown

    Args:
        body (HwpToMarkdownFilesBody):
        body (HwpToMarkdownJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HwpMarkdownResult | Problem]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToMarkdownFilesBody | HwpToMarkdownJsonBody | Unset = UNSET,
) -> HwpMarkdownResult | Problem | None:
    """HWP/HWPX to Markdown

    Args:
        body (HwpToMarkdownFilesBody):
        body (HwpToMarkdownJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HwpMarkdownResult | Problem
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
