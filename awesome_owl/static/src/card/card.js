import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        body: { type: String, optional: true },
        slots: {
            type: Object,
            optional: true,
            shape: {
                default: { optional: true },
            },
        },
        toggleMode: {
            type: Boolean,
        }
    };

    setup() {
        this.state = useState({
            isToggleOn: false
        });
    }

    toggle() {
        if (this.props.toggleMode) {
            this.state.isToggleOn = !this.state.isToggleOn;
        }
    }
}
