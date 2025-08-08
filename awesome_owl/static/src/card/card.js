/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: {type: String},
        slots: {
            type: Object,
            default: true,
        }
    };
    
    setup() {
        this.state = useState({ isopen : true });
    }

    toggleCard() {
        this.state.isopen = !this.state.isopen;
    }
}
