
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component } from "@odoo/owl";

export class DashboardLoader extends Component {
    static template = "awesome_dashboard.DashboardLoader"
    static components = { LazyComponent };
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardLoader);
