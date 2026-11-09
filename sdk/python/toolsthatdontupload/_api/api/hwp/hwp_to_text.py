from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hwp_text_result import HwpTextResult
from ...models.hwp_to_text_files_body import HwpToTextFilesBody
from ...models.hwp_to_text_json_body import HwpToTextJsonBody
from ...models.problem import Problem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: HwpToTextFilesBody | HwpToTextJsonBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/hwp/text",
    }

    if isinstance(body, HwpToTextFilesBody):
        _kwargs["files"] = body.to_multipart()

    if isinstance(body, HwpToTextJsonBody):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> HwpTextResult | Problem | None:
    if response.status_code == 200:
        response_200 = HwpTextResult.from_dict(response.json())

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
) -> Response[HwpTextResult | Problem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToTextFilesBody | HwpToTextJsonBody | Unset = UNSET,
) -> Response[HwpTextResult | Problem]:
    """HWP/HWPX to text and structured blocks

    Args:
        body (HwpToTextFilesBody):
        body (HwpToTextJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HwpTextResult | Problem]
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
    body: HwpToTextFilesBody | HwpToTextJsonBody | Unset = UNSET,
) -> HwpTextResult | Problem | None:
    """HWP/HWPX to text and structured blocks

    Args:
        body (HwpToTextFilesBody):
        body (HwpToTextJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HwpTextResult | Problem
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToTextFilesBody | HwpToTextJsonBody | Unset = UNSET,
) -> Response[HwpTextResult | Problem]:
    """HWP/HWPX to text and structured blocks

    Args:
        body (HwpToTextFilesBody):
        body (HwpToTextJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HwpTextResult | Problem]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToTextFilesBody | HwpToTextJsonBody | Unset = UNSET,
) -> HwpTextResult | Problem | None:
    """HWP/HWPX to text and structured blocks

    Args:
        body (HwpToTextFilesBody):
        body (HwpToTextJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HwpTextResult | Problem
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
