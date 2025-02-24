import { Component,useState} from "@odoo/owl";

export class Card extends Component{

    static template = "awesome_owl.Card";
    static props = {
        title: { type: String, optional: true },
        // content: { type: String, optional: false }
        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    };
}
