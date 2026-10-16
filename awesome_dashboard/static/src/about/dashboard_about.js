import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class DashboardAbout extends Component {
    static template = xml`
            <div>
                About Page
            </div>
        `;
}

registry
    .category("lazy_components")
    .add("awesome_dashboard.about_component", DashboardAbout);
