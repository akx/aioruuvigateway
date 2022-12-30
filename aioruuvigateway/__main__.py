import argparse
import asyncio
import dataclasses
import json
import logging

import httpx

from aioruuvigateway.api import get_gateway_history_data
from aioruuvigateway.models import TagData

log = logging.getLogger(__name__)


def json_default(o):
    if isinstance(o, bytes):
        return o.hex()
    raise TypeError(f"Object {o!r} is not JSON serializable")


def dump_tag_json(tag: TagData, *, parse: bool) -> str:
    data = dataclasses.asdict(tag)
    if parse:
        data["parsed"] = dataclasses.asdict(tag.parse_announcement())
    return json.dumps(
        data,
        ensure_ascii=False,
        default=json_default,
    )


async def run(
    host: str,
    token: str,
    interval: int,
    parse: bool = False,
    output_json: bool = False,
) -> None:
    async with httpx.AsyncClient() as client:
        last_tag_datas: dict[str, TagData] = {}
        while True:
            data = await get_gateway_history_data(
                client,
                host=host,
                bearer_token=token,
            )
            n_new = 0
            for tag in data.tags:
                if (
                    tag.mac not in last_tag_datas
                    or last_tag_datas[tag.mac].data != tag.data
                ):
                    try:
                        if output_json:
                            print(dump_tag_json(tag, parse=parse))
                        else:
                            print(tag)
                            if parse:
                                print("  ", tag.parse_announcement())
                    except Exception:
                        log.exception("Error printing tag %s", tag.mac)
                    last_tag_datas[tag.mac] = tag
                    n_new += 1
            if not n_new:
                log.info("No new data")
            await asyncio.sleep(interval)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Log Ruuvi Gateway history data",
    )
    ap.add_argument("--host", required=True)
    ap.add_argument("--token", required=True)
    ap.add_argument("--interval", type=int, default=5)
    ap.add_argument("--json", action="store_true", help="Output JSON")
    ap.add_argument("--parse", action="store_true", help="Parse advertisement data")
    args = ap.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    asyncio.run(
        run(
            host=args.host,
            token=args.token,
            interval=args.interval,
            parse=args.parse,
            output_json=args.json,
        )
    )


if __name__ == "__main__":
    main()
