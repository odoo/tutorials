/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: { type: Object, optional: true },
    };

    setup() {
        this.isOpen = useState({ value: true });
    }
}
