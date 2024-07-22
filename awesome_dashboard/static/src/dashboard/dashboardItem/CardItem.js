/** @odoo-module */

import { Component } from "@odoo/owl";

export class CardItem extends Component {
    static template = "awesome_dashboard.CardItem";
    static props = {
        title: {
            type: String,
        },
        value: {
            type: Number,
        },
    };
}
