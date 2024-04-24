/** @odoo-module **/

import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

class DashboardAction extends Component {
    static components = { LazyComponent }
    static template = xml`
    <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'awesome_dashboard'" props="props"/>
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardAction);
