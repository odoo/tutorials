/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "my_module.Card";

    static props = {
        title: {type: String},
        content: {type: String, optional: true}
    }
}