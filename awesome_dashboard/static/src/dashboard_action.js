import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component } from "@odoo/owl";

class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static template = "awesome_dashboard.bundle";
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
