import { Component, xml } from "@odoo/owl";
import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";

class DashboardComponentLoader extends Component {
    static components = { LazyComponent };
    static props = ["*"];
    static template = xml`
    <LazyComponent bundle="'awesome_dashboard.dashboard_assets'" Component="'AwesomeDashboard'" />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardComponentLoader);
