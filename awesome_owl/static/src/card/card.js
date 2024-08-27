/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: {type: String},
        content: {type: String, optional: true},
        slots: {type: Object, optional: true},
    };

    setup() {
        this.state = useState({visible: true});
    }

    hide() {
        this.state.visible = !this.state.visible;
    }
}
