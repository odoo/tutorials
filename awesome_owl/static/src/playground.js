import { Component, markup } from "@odoo/owl";
import { Card } from "./components/card/card";
import { Counter } from "./components/counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.card1Body = "<div>text without markup</div>";
        this.card2Body = markup("<div>text with markup</div>");
    }
}
