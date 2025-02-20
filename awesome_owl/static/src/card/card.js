import { Component, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = { title: String, slots: { type: Object, optional: true } };
}
