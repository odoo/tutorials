import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

export class AboutLoader extends Component {
    static components = { LazyComponent };

    static template = xml`
        <LazyComponent 
            bundle="'awesome_dashboard.about'" 
            Component="'awesome_dashboard.about_component'"
        />
    `;
}

registry
    .category("actions")
    .add("awesome_dashboard.dashboard_about", AboutLoader);
