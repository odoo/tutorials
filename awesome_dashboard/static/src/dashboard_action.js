import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

export class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static template = "awesome_dashboard.AwesomeDashboardLoader";

    setup() {}
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
