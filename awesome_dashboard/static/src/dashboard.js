/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout };
    static props = {};

    setup() {
        this.action = useService("action");
        this.title = "Awesome Dashboard";
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
