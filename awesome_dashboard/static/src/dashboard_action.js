/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'"/>
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
