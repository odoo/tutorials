import { LazyComponent } from "@web/core/assets";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { AwesomeDashboard } from "./components/dashboard/dashboard";
import { xml } from "@odoo/owl";

export class ExampleComponentLoader extends Component {
    static components = { LazyComponent, AwesomeDashboard };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", ExampleComponentLoader);
