import { Component, useState, validate } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        isOpened: Boolean,
        slots: {
            type: Object, shape: {
                default: { type: Object, optional: true }
            }
        }
    }
}
