import { Component, xml } from "@odoo/owl";
import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";


export class DashboardLoader extends Component {
    static components = { LazyComponent };
    static template = "awesome_dashboard.DashboardLoader"
}

registry.category("actions").add("awesome_dashboard.dashboard_action", DashboardLoader);
