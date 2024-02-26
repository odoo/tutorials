/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ClientAction extends Component {
  static template = "awesome_clicker.client_action";

  setup() {
    this.clickerService = useState(
      useService("awesome_clicker.clickerService")
    );
  }

  increment = () => this.clickerService.increment(9);
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
