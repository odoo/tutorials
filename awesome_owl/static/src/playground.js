import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    setup() {
        this.withMarkup = markup("<div class='text-success fw-bold'> With Markup HTML </div>");
        this.withoutMarkup = "<div class='text-danger fw-bold'> Without Markup </div>";
    }
}
