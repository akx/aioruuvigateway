from __future__ import annotations

import dataclasses
import datetime

from bluetooth_data_tools import BLEGAPAdvertisement, parse_advertisement_data


class TimestampConversionMixin:
    timestamp: int

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self.timestamp)


@dataclasses.dataclass()
class TagData(TimestampConversionMixin):
    mac: str  # AA:BB:CC:DD:EE:FF
    rssi: int
    timestamp: int
    data: bytes
    age_seconds: int | None = None

    def parse_announcement(self) -> BLEGAPAdvertisement:
        return parse_advertisement_data([self.data])

    @classmethod
    def from_gateway_history_json_tag(
        cls,
        mac: str,
        data: dict,
        response_timestamp: int | None,
    ) -> TagData:
        tag_timestamp = int(data["timestamp"])
        age_seconds = (
            (response_timestamp - tag_timestamp) if response_timestamp else None
        )
        return cls(
            mac=mac,
            rssi=int(data["rssi"]),
            timestamp=tag_timestamp,
            data=bytes.fromhex(data["data"]),
            age_seconds=age_seconds,
        )


@dataclasses.dataclass()
class HistoryResponse(TimestampConversionMixin):
    timestamp: int
    gw_mac: str
    tags: list[TagData]
    coordinates: str = ""

    @property
    def gw_mac_suffix(self) -> str:
        return self.gw_mac[-5:].upper()

    @classmethod
    def from_gateway_history_json(cls, data: dict) -> HistoryResponse:
        data = data["data"]
        response_timestamp = int(data["timestamp"])
        tags = [
            TagData.from_gateway_history_json_tag(
                mac=mac,
                data=tag_data,
                response_timestamp=response_timestamp,
            )
            for mac, tag_data in data.get("tags", {}).items()
        ]
        return HistoryResponse(
            timestamp=response_timestamp,
            gw_mac=data["gw_mac"],
            coordinates=data.get("coordinates", ""),
            tags=tags,
        )
