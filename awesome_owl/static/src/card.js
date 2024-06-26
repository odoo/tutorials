/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        content: String,
        slots: Object,
        is_toggled: {
            type: Boolean,
            optional: true
        }
    };

    setup() {
        this.state = useState({ value: this.props.is_toggled });
    }

    toggle(){
        this.state.value = !this.state.value;
    }
}
