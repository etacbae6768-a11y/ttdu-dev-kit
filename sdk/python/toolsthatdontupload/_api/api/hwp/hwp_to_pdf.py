from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hwp_to_pdf_files_body import HwpToPdfFilesBody
from ...models.hwp_to_pdf_json_body import HwpToPdfJsonBody
from ...models.problem import Problem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: HwpToPdfFilesBody | HwpToPdfJsonBody | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/hwp/pdf",
    }

    if isinstance(body, HwpToPdfFilesBody):
        _kwargs["files"] = body.to_multipart()

    if isinstance(body, HwpToPdfJsonBody):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Problem | None:
    if response.status_code == 501:
        response_501 = Problem.from_dict(response.json())

        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[Problem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToPdfFilesBody | HwpToPdfJsonBody | Unset = UNSET,
) -> Response[Problem]:
    """Not available on the server (501 browser_only)

     Page rendering needs fonts and runs in the browser: https://dagotools.com/en/tools/hwp-to-pdf/ .
    Always answers 501 on the hosted API, before any quota is used.

    Args:
        body (HwpToPdfFilesBody):
        body (HwpToPdfJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Problem]
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
    body: HwpToPdfFilesBody | HwpToPdfJsonBody | Unset = UNSET,
) -> Problem | None:
    """Not available on the server (501 browser_only)

     Page rendering needs fonts and runs in the browser: https://dagotools.com/en/tools/hwp-to-pdf/ .
    Always answers 501 on the hosted API, before any quota is used.

    Args:
        body (HwpToPdfFilesBody):
        body (HwpToPdfJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Problem
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToPdfFilesBody | HwpToPdfJsonBody | Unset = UNSET,
) -> Response[Problem]:
    """Not available on the server (501 browser_only)

     Page rendering needs fonts and runs in the browser: https://dagotools.com/en/tools/hwp-to-pdf/ .
    Always answers 501 on the hosted API, before any quota is used.

    Args:
        body (HwpToPdfFilesBody):
        body (HwpToPdfJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Problem]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: HwpToPdfFilesBody | HwpToPdfJsonBody | Unset = UNSET,
) -> Problem | None:
    """Not available on the server (501 browser_only)

     Page rendering needs fonts and runs in the browser: https://dagotools.com/en/tools/hwp-to-pdf/ .
    Always answers 501 on the hosted API, before any quota is used.

    Args:
        body (HwpToPdfFilesBody):
        body (HwpToPdfJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Problem
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
