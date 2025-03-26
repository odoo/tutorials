import { Component } from "@odoo/owl";

export default class Card extends Component {
    static template = "awesome_owl.Card";

    static props = {
        title: { type: String },
        content: { type: String,Object }, 
    };
}
