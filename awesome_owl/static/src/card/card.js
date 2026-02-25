import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: String,
        slots: Object
    }

    setup() {
        super.setup();

        this.state = useState({
            open: true,
        })
    }

    toggleOpen() {
        this.state.open = !this.state.open;
    }
}