/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useExternalListener } from "@odoo/owl";

export class ClientAction extends Component {
  static template = "awesome_clicker.client_action";
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
