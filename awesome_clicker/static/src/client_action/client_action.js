/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useClicker } from "../clicker_hook";
import { ClickerValue } from "../clicker_value/clicker_value";
import { Notebook } from "@web/core/notebook/notebook";

export class ClientAction extends Component {
  static template = "awesome_clicker.client_action";
  static components = { ClickerValue, Notebook };

  setup() {
    this.clicker = useClicker();
  }

  increment = () => this.clicker.increment(9);
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
