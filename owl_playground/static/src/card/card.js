/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {}

Card.template = "owl_playground.card";
Card.props = {
    list: {
        type: Array,
        element: {type: Object, id : {type: Number}, description : {type: String}, done : {type: Boolean}},
    },
    slots: {
        type: Object,
        shape: {
            default: Object,
            title: { optional: true },
        },
    }
};
