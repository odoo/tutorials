/** @odoo-module **/

import { Component, useState} from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String, optional: true },
        slots: { type: Object, shape: {
            default: true
        }},
    }
    setup() {
        this.title = this.props.title;
        this.isOpen = useState({value: false});
    }

    onClick() {
     console.log(`Card ${this.title} clicked`)
    }

    toggleOpen() {
        this.isOpen.value = !this.isOpen.value;
    }
}
