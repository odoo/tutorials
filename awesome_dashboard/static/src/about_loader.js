import { Component, xml } from "@odoo/owl";
import { LazyComponent } from "@web/core/assets";
import { registry } from "@web/core/registry";

class AboutLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'awesome_dashboard.about'" Component="'AboutPage'" />
    `;
}

registry.category("actions").add("awesome_dashboard.about", AboutLoader);
