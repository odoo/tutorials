/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: { type: String, optional: true, default: "Card Title" },
        content: { type: String, optional: true, default: "Card Content" },
    };
}