import { Component ,xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";


export class DashboardLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'awesome_dashboard.dashboard'" />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardLoader);