/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = 'awesome_owl.card';
    static props = {
        title: {type: String},
        slots: Object,
    };

    setup() {
        this.state = useState({open: true});
    }

    toggleOpen() {
        this.state.open = !this.state.open;
    }
}
