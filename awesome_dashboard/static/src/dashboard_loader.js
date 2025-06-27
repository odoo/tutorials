/** @odoo-module **/
import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { AwesomeDashboard } from "./dashboard/dashboard";


export class AwesomeDashboardLoader extends Component {
    static components = {LazyComponent, AwesomeDashboard};
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'awesome_dashboard.dashboard'" />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
