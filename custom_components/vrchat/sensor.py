"""Sensor platform for VRChat Friends."""
import logging
from datetime import timedelta

import async_timeout
import aiohttp

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, VRCHAT_API_URL, USER_AGENT

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = VRChatDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([VRChatFriendsSensor(coordinator, entry)])


class VRChatDataUpdateCoordinator(DataUpdateCoordinator):
    """A coordinator to fetch data from the VRChat API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.auth_cookie = entry.data["auth_cookie"]
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> list:
        """Fetch data from the VRChat API."""
        headers = {"User-Agent": USER_AGENT, "Cookie": self.auth_cookie}
        session = async_get_clientsession(self.hass)

        try:
            async with async_timeout.timeout(15):
                async with session.get(VRCHAT_API_URL, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()

                    processed_friends = []
                    for friend in data:
                        if friend.get("platform") != "web":
                            # Prioritize banner > avatar > icon
                            friend["display_pic"] = (
                                friend.get("profilePicOverride")
                                or friend.get("currentAvatarThumbnailImageUrl")
                                or friend.get("userIcon")
                                or ""
                            )
                            processed_friends.append(friend)
                    return processed_friends
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with VRChat API: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching VRChat data")
            raise UpdateFailed(f"An unexpected error occurred: {err}") from err


class VRChatFriendsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a VRChat Friends Sensor."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: VRChatDataUpdateCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Online Friends"
        self._attr_unique_id = f"{entry.entry_id}_online_friends"
        self._attr_icon = "mdi:account-multiple"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "friends"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "VRChat",
            "manufacturer": "VRChat Inc.",
            "entry_type": "service",
        }

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        return len(self.coordinator.data) if self.coordinator.data else 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {"online_list": self.coordinator.data}