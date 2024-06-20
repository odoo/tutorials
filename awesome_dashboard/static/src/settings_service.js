/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const settingsService = {
  dependencies: ["user"],
  start(env, { user }) {
    const storedSettings = JSON.parse(
      user.settings?.awesome_dashboard_settings || "null",
    );
    const settings = reactive(
      storedSettings ?? {
        disabledItems: [],
      },
    );

    return {
      settings,
      setDisabledItems(newDisabledItems) {
        settings.disabledItems = newDisabledItems;
        user.setUserSettings(
          "awesome_dashboard_settings",
          JSON.stringify(settings),
        );
      },
    };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.settings", settingsService);
