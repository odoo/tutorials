/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class AwesomeDashboardAction extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" props="props"/>
    `;

}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardAction);