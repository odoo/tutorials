import { Component, xml, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/lazy_component";


export class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    props = useProps();
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" props="this.props" />
    `;
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
