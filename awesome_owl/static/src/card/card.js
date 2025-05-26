import { Component, useState, useRef } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    };

    setup() {
        this.state = useState({ isOpen: true });
        this.toggleButtonRef = useRef('ToggleButton');
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
        this.toggleButtonRef.el.textContent = this.state.isOpen ? "Close" : "Open";
    }
}