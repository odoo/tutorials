import { Component } from "@odoo/owl";

export class Card extends Component {
    static props = {
        title: { type: String,},
        content: { type: String}
    };
    static template = "awesome_owl.card"
}
