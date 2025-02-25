import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    setup() {
        this.state = useState({ open: true });
    }
    toggle() {
        this.state.open = !this.state.open
        console.log(this.state.open)
        console.log("TOGGLED")

    }
    static template = "awesome_owl.card"
    static props = ['title', 'slots?']
}
