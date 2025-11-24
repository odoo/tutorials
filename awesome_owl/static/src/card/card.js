import { Component, useState } from "@odoo/owl";

class Card extends Component {
    static template = "awesome_owl.card"
    static props = {
        title: {type: String},
        content: {type: String},
        slots: {type: Object, optional: true}
    }

    setup() {
        this.state = useState({ open: true });
    }

    toggleOpen() {
        this.state.open = !this.state.open;
    }
}

export default Card;
