import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

class Testy extends Component {
    static template = xml`
    <h1>hehe</h1>
    `;
}

registry.category("actions").add("awesome_dashboard.testy", Testy);
