/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dashboard } from "./dashboard/dash_board";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Dashboard }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
