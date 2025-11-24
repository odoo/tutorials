import { Component } from "@odoo/owl";

class Card extends Component {
    static template = "awesome_owl.card"
    static props = {
        title: {type: String},
        content: {type: String},
    }
}

export default Card;
