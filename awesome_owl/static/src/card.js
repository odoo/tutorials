import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String, validate: s => s.length < 10 },
        slots: { type: Object },
    };

    setup() {
        this.state = useState({ is_minimized: false });
    }

    toggleMinimize() {
        this.state.is_minimized = !this.state.is_minimized;
    }
}