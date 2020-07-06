from homeassistant import config_entries
from collections import OrderedDict
from .auth import get_master_token
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_MASTER_TOKEN, CONF_DEVICE_TYPES, CONF_RSSI_THRESHOLD, CONF_TRACK_ALARMS, CONF_TRACK_DEVICES, DEFAULT_DEVICE_TYPES, DEFAULT_RSSI_THRESHOLD

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

@staticmethod
@callback
def async_get_options_flow(config_entry):
    return GoogleHomeOptionsFlow()

class GoogleHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input):
        errors = {}
        if user_input is not None:
            mt = get_master_token(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if mt is not None:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data={
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_MASTER_TOKEN: mt,
                    },
                    options={
                        CONF_RSSI_THRESHOLD: DEFAULT_RSSI_THRESHOLD,
                        CONF_DEVICE_TYPES: DEFAULT_DEVICE_TYPES,
                        CONF_TRACK_DEVICES: True,
                        CONF_TRACK_ALARMS: False,
                    }
                )

        data_schema = OrderedDict()
        data_schema[vol.Required(CONF_USERNAME)] = str
        data_schema[vol.Required(CONF_PASSWORD)] = str

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema(data_schema),
            errors=errors
        )

class GoogleHomeOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_update_entry(entry=self.config_entry, options=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_RSSI_THRESHOLD,
                        default=self.config_entry.options.get(CONF_RSSI_THRESHOLD),
                    ): vol.Coerce(int),
                    vol.Required(
                        CONF_DEVICE_TYPES,
                        default=self.config_entry.options.get(CONF_DEVICE_TYPES),
                    ): vol.All(
                        cv.ensure_list, [vol.In(DEFAULT_DEVICE_TYPES)]
                    ),
                    vol.Required(CONF_TRACK_ALARMS, default=False): cv.boolean,
                    vol.Required(CONF_TRACK_DEVICES, default=True): cv.boolean,
                }
            ),
        )
 