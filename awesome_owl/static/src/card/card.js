import { useState, Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: {type: Object, optional: true},
    };

    setup() {
        this.state = useState({ visible: true });
    }

    toggleVisible() {
        this.state.visible = !this.state.visible;
    }
}
