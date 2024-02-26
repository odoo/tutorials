/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

export class ClickerSystray extends Component {
  static template = "awesome_clicker.ClickerSystray";

  setup() {
    this.state = useState({ count: 0 });
  }

  increment = () => this.state.count++;
}

export const systrayItem = {
  Component: ClickerSystray,
};
registry
  .category("systray")
  .add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });
