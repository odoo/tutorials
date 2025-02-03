/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card"
    static props= {
        title: {type: String},
        content: {type: String, optional: true},
        slots: {type: Object}
    }

    setup() { //constuctor
        this.state = useState({ isToggleShow: false });
    }

    toggleShow() {
        console.log(this.state.isToggleShow)
        this.state.isToggleShow= !this.state.isToggleShow
    }
}
