import { Component, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        slots: {
            type: Object,
            shape: {
                default: {}
            }
        }
    };

    setup() {
        this.state = useState([{
            isOpen: false
        }])
    }

    toggleCard() {
        this.state.isOpen = !this.state.isOpen
    }
}
