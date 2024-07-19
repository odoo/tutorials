/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String },
        "*": true,
    };

    setup() {
        this.showContent = useState({ value: true });
    }

    toggleShowContent() {
        this.showContent.value = !this.showContent.value;
    }
}
