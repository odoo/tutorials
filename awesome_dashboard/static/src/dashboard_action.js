import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

class DashboardLoader extends Component {
    static template = "awesome_dashboard.DashboardLoader";
    static components = { LazyComponent };
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardLoader);
