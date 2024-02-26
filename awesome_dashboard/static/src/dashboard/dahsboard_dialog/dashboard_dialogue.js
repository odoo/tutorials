/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { useService } from "@web/core/utils/hooks";

export class ConfigurationDialog extends Component {
  static template = "awesome_dashboard.ConfigurationDialog";
  static components = { Dialog, CheckBox };
  static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

  setup() {
    this.orm = useService("orm");
    this.user = useService("user");

    this.items = useState(
      this.props.items.map((item) => {
        return {
          ...item,
          enabled: !this.props.disabledItems.includes(item.id),
        };
      })
    );
  }

  done() {
    this.props.close();
  }

  onChange(checked, changedItem) {
    changedItem.enabled = checked;
    const newDisabledItems = Object.values(this.items)
      .filter((item) => !item.enabled)
      .map((item) => item.id);
    this.user.setUserSettings("stats_visibility", newDisabledItems);

    this.props.onUpdateConfiguration(newDisabledItems);
  }
}
