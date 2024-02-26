/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useClicker } from "../clicker_hook";

export class ClientAction extends Component {
  static template = "awesome_clicker.client_action";

  setup() {
    this.clicker = useClicker();
  }

  increment = () => this.clicker.increment(9);
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
