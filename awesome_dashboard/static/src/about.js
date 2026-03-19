import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

class About extends Component {
    static template = xml`
    <div class="text-danger"> HELLLEO</div>
    `;
}

registry.category("actions").add("awesome_dashboard.about", About);
