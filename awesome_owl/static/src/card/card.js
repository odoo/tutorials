/** @odoo-module **/
import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card"; // Reference to the template
    static props = {
        title: { type: String },   // title must be a string
        content: { type: String }, // content must be a string
    };
}
