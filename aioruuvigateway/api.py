from __future__ import annotations

import httpx

from aioruuvigateway.excs import CannotConnect, InvalidAuth
from aioruuvigateway.models import HistoryResponse


async def get_gateway_history_data(
    client: httpx.AsyncClient,
    host: str,
    bearer_token: str,
    timeout: int | None = None,
) -> HistoryResponse:
    try:
        resp = await client.get(
            url=f"http://{host}/history",
            headers={
                "Authorization": f"Bearer {bearer_token}",
            },
            timeout=(timeout if timeout else httpx.USE_CLIENT_DEFAULT),
        )
        if resp.status_code == 200:
            return HistoryResponse.from_gateway_history_json(resp.json())
        resp.raise_for_status()
    except httpx.HTTPStatusError as err:
        if err.response.status_code == 401:
            raise InvalidAuth from err
        raise CannotConnect from err
    except Exception as err:  # pragma: no cover
        raise CannotConnect from err
    raise NotImplementedError("This should not happen")
