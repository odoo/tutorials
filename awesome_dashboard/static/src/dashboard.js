import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
}

class AwesomeDashboardWrapper extends Component {
    static template = "awesome_dashboard.AwesomeDashboardWrapper";
    static components = { Layout, AwesomeDashboard };

    get layoutProps() {
        return {
            controlPanel: {},       // empty control panel
            className: "o_dashboard h-100", // proper string
        };
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardWrapper);
