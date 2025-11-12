/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title : String,
        message : String,
        slots : {type: Object, optional: true}
    }
    setup() {
        this.isMinimized = useState({ value: false });
    }
    cardMinMaximize() {
        this.isMinimized.value = !this.isMinimized.value;
    }
}
