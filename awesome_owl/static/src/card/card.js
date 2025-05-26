import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";
    static props = {
        "title": {
            type: String,
            validate: s => s.startsWith("[Odoo]")
        },
        "content": String
    }
}
