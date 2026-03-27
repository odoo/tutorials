import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    static props = {
        title: {type: String},
        slots: {optional: true},
    }

    setup(){
        this.state = useState({isOpen: true})
    }

    toggle(){
        this.state.isOpen = !this.state.isOpen;
    }
}