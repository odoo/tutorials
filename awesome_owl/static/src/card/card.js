/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: {type: String},
        slots: {type: Object, shape: {default: true}}
    }

    setup() {
        this.show_content = useState({show: true});
    }

    toggleContent() {
        this.show_content.show = !this.show_content.show;
    }
}
