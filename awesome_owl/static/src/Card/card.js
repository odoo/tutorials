import { Component } from "@odoo/owl";

export class Card extends Component {

    static props = {
        title: String,
        content: { type: String, optional: true},
    };

    static template = "awesome_owl.card";
}
