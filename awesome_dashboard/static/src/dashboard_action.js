/** @odoo-module **/

import { Component } from "@odoo/owl";
import { AwesomeDashboard } from "./dashboard/dashboard";
import { registry } from "@web/core/registry";

export class LazyLoader extends Component {
    static components = { AwesomeDashboard };
    static template = "awesome_dashboard.lazy_component";
}

registry.category("actions").add("awesome_dashboard.dashboard", LazyLoader);  