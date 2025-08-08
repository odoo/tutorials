/** @odoo-module **/

import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    static props = {
        title: String,
        slots: {
            type: Object,
            optional: true
        }
    }
    static template = "awesome_owl.card";

    state = useState({ visibility: true })

    toggleState() {
        this.state.visibility = !this.state.visibility
    }
}
