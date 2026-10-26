import { Component, useProps, xml } from "@odoo/owl";
import { LazyComponent } from "@web/core/lazy_component";
import { registry } from "@web/core/registry";

export class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
    <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" props="this.props"/>
    `;
    props = useProps();
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);