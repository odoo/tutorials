import {Component, useState} from "@odoo/owl";

export class Card extends Component{

    static template = "awesome_owl.Card"
    static props = {
        title: { type: String, optional: true },
        description: { type: String, optional: true },
        slots: {
            type: Object,
            shape: {
                default: true
            }
        }
    }

    setup() {
        this.state = useState({isOpen: true})
    }

    toggleVisibility() {
        this.state.isOpen = !this.state.isOpen
    }

}
