/** @odoo-module **/

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

export class DashboardLoader extends Component {
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'awesome_dashboard.AwesomeDashboard'" />
    `;
    
    static components = { LazyComponent };  // ✅ Ensure LazyComponent is registered
}

// ✅ Register `DashboardLoader` in `actions`
registry.category("actions").add("awesome_dashboard.dashboard", DashboardLoader);
