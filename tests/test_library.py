from collections import Counter
from pathlib import Path

import httpx
import pytest

from aioruuvigateway.api import get_gateway_history_data
from aioruuvigateway.excs import InvalidAuth

example_path = Path(__file__).parent / "example.json"


@pytest.mark.asyncio
async def test_library(httpx_mock):
    httpx_mock.add_response(
        url="http://192.168.1.202/history",
        content=example_path.read_bytes(),
        headers={"Content-Type": "application/json"},
    )
    async with httpx.AsyncClient() as client:
        history = await get_gateway_history_data(
            client=client,
            host="192.168.1.202",
            bearer_token="bear, a scary bear",
        )
    assert history.gw_mac_suffix == "EE:FF"
    manufacturers = Counter()
    for tag in history.tags:
        assert tag.datetime.year == 2022
        ann = tag.parse_announcement()
        print(ann)
        manufacturers.update(ann.manufacturer_data.keys())
    assert manufacturers == {
        0x0499: 2,  # Two Ruuvitags
        0x012D: 1,  # One Sony
        0x004C: 1,  # One Apple
    }


@pytest.mark.asyncio
async def test_auth(httpx_mock):
    httpx_mock.add_response(
        url="http://192.168.1.202/history",
        status_code=401,
    )
    async with httpx.AsyncClient() as client:
        with pytest.raises(InvalidAuth):
            await get_gateway_history_data(
                client=client,
                host="192.168.1.202",
                bearer_token="not good at all",
            )
