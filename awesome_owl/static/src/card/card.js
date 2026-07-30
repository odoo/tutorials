import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        id: Number,
        title: String,
        isCrossedOut: Boolean,
        toggleState: {
            Function, optional: true
        },
        removeTodo: {
            Function, optional: true
        },
        slots: Object
    }

    setup() {
        this.state = useState({
            isCrossed: this.props.isCrossedOut,
            isOpen: false
        })
    }

    toggleState(event) {
        this.state.isCrossed = !this.state.isCrossed;
        this.props.toggleState(this.props.id);
    }

    removeTodo(event) {
        this.props.removeTodo(this.props.id);
    }

    toggleCard(event) {
        this.state.isOpen = !this.state.isOpen
    }
}