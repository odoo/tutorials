import {Component, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        text: String,
        title: String,
        slots: {optional: true},
    }

    setup() {
        this.state = useState({
            open: true
        })
    }

    toggleState() {
        this.state.open = !this.state.open;
    }
}