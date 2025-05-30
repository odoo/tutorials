import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        "title": {
            type: String,
            validate: s => s.startsWith("[Odoo]")
        },
        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    }

    setup() {
        this.state = useState({value: true});
    }

    toggleState() {
        this.state.value = !this.state.value;
    }
}
