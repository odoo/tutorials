import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String },
        slots: Object
    };

    setup() {
        this.expanded = useState({ value: true });
    }

    toggle() {
        this.expanded.value = !this.expanded.value;
    }
}
