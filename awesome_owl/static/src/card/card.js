import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "my_module.Card";

    static props = {
        title: {type: String},
        slots: {type: Object, optional: true}
    }

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleCardBody() {
        this.state.isOpen = !this.state.isOpen;
    }
}
