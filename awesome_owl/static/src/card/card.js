/** @odoo-module **/

import { Component } from "@odoo/owl";
export class Card extends Component {
    static template = "awesome_owl.card"

    static props = {
        title: String,
        slots: {
            type: Object, 
            shape: {
                default: true, 
            },
        },
    }
}
