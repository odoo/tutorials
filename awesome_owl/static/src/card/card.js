/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = [ "slots?" ];
    setup() {
        this.isOpen = useState({value: false});
    }

    toggleOpen() {
        this.isOpen.value = !this.isOpen.value;
    }
}
