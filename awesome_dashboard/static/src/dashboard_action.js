/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

export class DashboardAction extends Component {
    static components = { LazyComponent };
    static template = "awesome_dashboard.DashboardAction";
}

// Register the loader in the actions registry
registry.category("actions").add("awesome_dashboard.dashboard_action", DashboardAction);
