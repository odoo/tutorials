import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component } from "@odoo/owl";

class AwesomeDashboardLoader extends Component {
    static template = "awesome_dashboard.AwesomeDashboardLoader";
    static components = { LazyComponent };
    static props = {};
}
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);