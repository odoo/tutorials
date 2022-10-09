/** @odoo-module **/

import { registry } from "@web/core/registry";

const { Component } = owl;

class AwesomeDashboard extends Component {}

AwesomeDashboard.components = {};
AwesomeDashboard.template = "awesome_tshirt.clientaction";

registry.category("actions").add("awesome_tshirt.dashboard", AwesomeDashboard);
