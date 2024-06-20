/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

export class ConfigurationDialog extends Component {
  static template = "awesome_dashboard.configuration_dialog";
  static components = { Dialog, CheckBox };
  static props = {
    items: {
      type: Array,
      value: String,
    },
    disabledItems: {
      type: Array,
      value: String,
    },
    onUpdateConfiguration: Function,
    close: Function,
  };

  setup() {
    this.items = useState(
      this.props.items.map((item) => ({
        ...item,
        enabled: !this.props.disabledItems.includes(item.id),
      })),
    );
  }

  onDoneClicked() {
    this.props.close();
  }

  onChange(checked, changedItem) {
    changedItem.enabled = checked;
    const newDisabledItems = Object.values(this.items)
      .filter((item) => !item.enabled)
      .map((item) => item.id);

    this.props.onUpdateConfiguration(newDisabledItems);
  }
}
