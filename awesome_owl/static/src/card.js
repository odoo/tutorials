/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {title: {type: String}, content: {type: String, optional: true}, slots: {type: Object}};

    setup() {
        this.state = useState({cardIsOpen: false});
    }

    toggleCard() {
        this.state.cardIsOpen = !this.state.cardIsOpen;
    }
}
