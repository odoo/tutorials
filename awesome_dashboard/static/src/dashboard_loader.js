import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/lazy_component";
import { Component, xml, useProps } from "@odoo/owl";

class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" props="this.props"/>
    `;
    props = useProps();
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
