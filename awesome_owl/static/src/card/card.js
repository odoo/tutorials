import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = { 
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true
            },
            optional: true,
        } 
    };

    setup() {
        this.state = useState({
            open: true,
            title: this.props.title,
        });
    }

    increment() {
        this.state.value++;
    }

    toggleOpen() {
        this.state.open = !this.state.open;
    }
}
