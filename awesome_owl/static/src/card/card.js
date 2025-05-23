/** @odoo-module **/

import { useState, Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: String,
        content: String
    };
}
