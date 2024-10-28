import { Component, markup, useState } from "@odoo/owl";


export class Card extends Component {
    static template = "card.card"
    static props = ["title", "content"];
    static props = {
        "title": {"type": String},
        "content": {"type": String},
    }

    // my_title = markup("<h1>Oh c'est un beau titre</h1>");
    // context = useState({"my_title": this.my_title});
}