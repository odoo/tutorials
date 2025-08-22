import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static props = { props: Object };
    static template = xml`<LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" props="props"/>`;
}
registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboardLoader);
