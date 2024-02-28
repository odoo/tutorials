/** @odoo-module **/

import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class DashboardAction extends Component {
    static components = { LazyComponent };
    static template = "awesome_dashboard.DashboardAction";
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardAction);
