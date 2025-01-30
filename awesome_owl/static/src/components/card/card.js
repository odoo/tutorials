/** @odoo-module **/

import { Component, useState } from "@odoo/owl"

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        slots: {
            type: Object,
            optional: true,
        }
    }

    setup() {
        this.state = useState({hidden: false})
    }

    hide() {
        this.state.hidden = !this.state.hidden;
    }
}
