/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    
    static props = {
        title: String,
        slots: {}
    };
    
    state = useState({isOpen: false});

    onToggle() {
        this.state.isOpen = !this.state.isOpen
    }
}