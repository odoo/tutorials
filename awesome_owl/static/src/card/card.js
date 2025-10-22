import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = ["title", "slots"];

    setup() {
        this.state = useState({ hidden: false });
    }

    toggle_visibility() {
        this.state.hidden = !this.state.hidden;
    }
}
