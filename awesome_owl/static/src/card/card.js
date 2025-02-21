import { Component } from "@odoo/owl";

export class Card extends Component{
    static props = {
        title: {type: String, optional: false},
        content: {type: [String,Object], optional: false},
    };
}

Card.template = "awesome_owl.card";