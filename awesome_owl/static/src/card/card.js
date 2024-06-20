/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    
    static template = "my_module.Card";

    static props = {
        title: {type: String},
        slots: { typ: Object, optional: true }
    }

    setup() {
        this.state = useState({ open: true });
    }

    toggleContent() {
        this.state.open = !this.state.open;
    }
}