/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {}

Card.template = "owl_playground.card";
Card.props = { // props are the inputs of the component
    slots: {
        type: Object, // the type of the prop is an object
        shape: { // the shape of the object is defined by the shape key
            default: Object, // default slot
            title: { type: Object, optional: true },
        },
    },
};