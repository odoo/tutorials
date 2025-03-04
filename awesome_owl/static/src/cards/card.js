import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static porps = {
        title: { type: String },
        content: { type: String }
    };   
}