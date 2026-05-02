import { Component, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class AwesomeCard extends Component {
    static template = "awesome_dashboard.AwesomeCard";
    static props = {
        size: { Number, default: 1 },
        value: { Number, default: 1 },
    }
}

registry.category("actions").add("awesome_dashboard.AwesomeCard", AwesomeCard);
