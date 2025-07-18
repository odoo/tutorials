/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component{
    static template = "awesome_owl.card";

    static props = {
        title: String,
        slots: { type: Object, optional: true } 
    };

    state = {
        isOpen: true,  
    };

    toggleContent() {
        console.log("toggleContent called");
        this.state.isOpen = !this.state.isOpen;
        console.log("state.isOpen:", this.state.isOpen);
    }
}