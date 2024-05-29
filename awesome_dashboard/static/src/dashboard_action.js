/** @odoo-module **/

import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

export class DashboardAction extends Component {
}

DashboardAction.template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" props="props"/>
    `;
DashboardAction.components = { LazyComponent };

registry.category("actions").add("awesome_dashboard.dashboard", DashboardAction);