/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook";

export class ClickerSystray extends Component {
  static template = "awesome_clicker.ClickerSystray";

  setup() {
    this.clicker = useClicker();
    this.actionService = useService("action");
  }

  openClickerView = () =>
    this.actionService.doAction({
      type: "ir.actions.client",
      tag: "awesome_clicker.client_action",
      target: "new",
      name: "Clicker",
    });

  increment = () => this.clicker.increment(9);
}

export const systrayItem = {
  Component: ClickerSystray,
};
registry
  .category("systray")
  .add("awesome_clicker.ClickerSystray", systrayItem, { sequence: 1000 });
