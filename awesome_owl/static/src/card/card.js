import { Component, useState} from "@odoo/owl";

export class Card extends Component{
    static template="awesome_owl.Card";
    static props = {
        title: String,
        content: { type: String, optional: true },
        slots: {
            type: Object,
            shape: { default: true },
            optional: true,
        }
    }

    setup(){
        this.state = useState({ isOpen: true})
    }

    toggleSlot(){
        this.state.isOpen = !this.state.isOpen;
    }
}
