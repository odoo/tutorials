/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: { type: String, optional: false, validate: x => x.length <= 10 },
        text: { type: String, optional: true, validate: x => x.length >= 10 },
        slots: { optional: true, },
    };

    setup() {
        this.state = useState({ hide: false, });
    }

    toggle() {
        this.state.hide = !this.state.hide;
    }
}
