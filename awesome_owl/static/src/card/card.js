import { Component, useState, onWillDestroy } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
        static props =  {
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
        onWillDestroy(() => {
            console.log("Card will be destroyed");
        });
    }

    toggleCard() {
        this.state.isOpen = !this.state.isOpen;
    }
}
