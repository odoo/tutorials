import { Component, xml } from "@odoo/owl";
import { LazyComponent } from "@web/core/assets";
import { AwesomeDashboard } from "./dashboard/dashboard";
import { registry } from "@web/core/registry";

class AwesomeDashboardLoader extends Component {
    static components = { 
        LazyComponent,
        AwesomeDashboard
     };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.awesome_bundle'" Component="'AwesomeDashboard'" />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);


