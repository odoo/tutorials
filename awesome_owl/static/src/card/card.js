/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: {type: String},
        slots: {type: Object},
        open: {type: Boolean, default: true, optional: true},
    };

    setup() {
        this.state = useState({ open: this.props.open });
    }

    toggleVisibility(){
        this.state.open = !this.state.open
    }
}
