/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ClickerSystray extends Component {
  static template = "awesome_clicker.ClickerSystray";

  setup() {
    this.state = useState({ count: 0 });
    this.actionService = useService("action");

    useExternalListener(
      window.document.body,
      "click",
      () => this.state.count++,
      { capture: true }
    );
  }

  openClickerView = () =>
    this.actionService.doAction({
      type: "ir.actions.client",
      tag: "awesome_clicker.client_action",
      target: "new",
      name: "Clicker",
    });

  increment = () => (this.state.count += 9);
}

export const systrayItem = {
  Component: ClickerSystray,
};
registry
  .category("systray")
  .add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });
