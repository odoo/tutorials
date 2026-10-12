import { Component, markup } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    setup() {
        this.footer = markup("<div class='fw-bold text-success'>This is the footer</div>");
    }

    static props = ["title", "content"]
}
