/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        toggle: {type: Boolean},
        slots: {
            type: Object,
            shape: {
                title: {type: Object, optional: true},
                header: {type: Object, optional: true},
                default: {type: Object},
            },
        },
    };

    setup() {
        this.toggle = useState({value: this.props.toggle});
    }

    toggleCard() {
        this.toggle.value = !this.toggle.value;
    }
}
