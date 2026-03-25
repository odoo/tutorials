import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { xml } from "@odoo/owl";

export class DashboardLoader extends Component {
    setup() {
        console.log("LOADER RUNNING ");
    }

    static components = { LazyComponent };

    static template = xml`
        <LazyComponent 
            bundle="'awesome_dashboard.dashboard'" 
            Component="'AwesomeDashboard'" 
        />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", DashboardLoader);