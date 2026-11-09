from http import HTTPStatus
from typing import Any

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.flow_run_json import FlowRunJson
from ...models.flow_run_multipart import FlowRunMultipart
from ...models.flow_run_result import FlowRunResult
from ...models.problem import Problem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: FlowRunMultipart | FlowRunJson | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/flows/run",
    }

    if isinstance(body, FlowRunMultipart):
        _kwargs["files"] = body.to_multipart()

    if isinstance(body, FlowRunJson):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> FlowRunResult | Problem | None:
    if response.status_code == 200:
        response_200 = FlowRunResult.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Problem.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Problem.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Problem.from_dict(response.json())

        return response_402

    if response.status_code == 413:
        response_413 = Problem.from_dict(response.json())

        return response_413

    if response.status_code == 415:
        response_415 = Problem.from_dict(response.json())

        return response_415

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
) -> Response[FlowRunResult | Problem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FlowRunMultipart | FlowRunJson | Unset = UNSET,
) -> Response[FlowRunResult | Problem]:
    """Run a saved flow on files

     Send the flow (ttdu.flow/v1, as exported from https://workflows.toolsthatdontupload.com/) and the
    files. To run a single tool, send a flow with one step. Steps that need a browser (for example
    image.batch) answer 422 on the hosted API.

    Args:
        body (FlowRunMultipart):
        body (FlowRunJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlowRunResult | Problem]
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
    body: FlowRunMultipart | FlowRunJson | Unset = UNSET,
) -> FlowRunResult | Problem | None:
    """Run a saved flow on files

     Send the flow (ttdu.flow/v1, as exported from https://workflows.toolsthatdontupload.com/) and the
    files. To run a single tool, send a flow with one step. Steps that need a browser (for example
    image.batch) answer 422 on the hosted API.

    Args:
        body (FlowRunMultipart):
        body (FlowRunJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlowRunResult | Problem
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FlowRunMultipart | FlowRunJson | Unset = UNSET,
) -> Response[FlowRunResult | Problem]:
    """Run a saved flow on files

     Send the flow (ttdu.flow/v1, as exported from https://workflows.toolsthatdontupload.com/) and the
    files. To run a single tool, send a flow with one step. Steps that need a browser (for example
    image.batch) answer 422 on the hosted API.

    Args:
        body (FlowRunMultipart):
        body (FlowRunJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FlowRunResult | Problem]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: FlowRunMultipart | FlowRunJson | Unset = UNSET,
) -> FlowRunResult | Problem | None:
    """Run a saved flow on files

     Send the flow (ttdu.flow/v1, as exported from https://workflows.toolsthatdontupload.com/) and the
    files. To run a single tool, send a flow with one step. Steps that need a browser (for example
    image.batch) answer 422 on the hosted API.

    Args:
        body (FlowRunMultipart):
        body (FlowRunJson):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FlowRunResult | Problem
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
