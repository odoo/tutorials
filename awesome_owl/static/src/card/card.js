/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = ['title', 'slots?'];

    setup() {
        this.state = useState({ open: false });
    }

    toggleContent(){
        this.state.open = ! this.state.open;
    }
}
