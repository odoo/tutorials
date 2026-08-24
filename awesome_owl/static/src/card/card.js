import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title : String,
        slots : { type: Object, optional: true}
    }

    setup() {
        this.state = useState({ open: false });
        this.changeState = this.changeState.bind(this)
    }

    changeState() {
        this.state.open = !this.state.open
    }
}
