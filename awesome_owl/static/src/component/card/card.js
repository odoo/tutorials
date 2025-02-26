/** @odoo-module **/

const { Component } = owl;

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        title: String,
        content: String
    }
}
