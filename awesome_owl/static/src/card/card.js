/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: { type: String },
        slots: { type: Object },
    };

    setup() {
        this.state = useState({ visible: true });
    }

    toggleVisible() {
        this.state.visible = !this.state.visible;
    }
}
