//addons/awesome_owl/static/src/card/card.js
import {Component, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: {type: String},
        slots: {type: Object},
    }

    setup() {
        this.state = useState({isOpen: {type: Boolean, default: true}});
    }

    toggle() {
        this.state.isOpen = !this.state.isOpen
    }
}
