/** @odoo-module */

const { Component } = owl;

export class Card extends Component {}

Card.template = "awesome_tshirt.Card";
Card.props = {    
    slots: {
        type: Object,
        shape: {
            default: Object,
            title: { type: Object, optional: true },
        },
    },
};