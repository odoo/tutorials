/** @odoo-module **/

import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    static template = "awesome_owl.card.card"
    static props = {
        title: String,
        slots: {
            type: Object
        }
    }

    setup() {
        this.state = useState({
            collapsed: false
        });
    }

    toggleCollapse() {
        this.state.collapsed = !this.state.collapsed;
    }
}