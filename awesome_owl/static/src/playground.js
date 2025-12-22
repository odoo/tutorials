import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.state = useState({ sum: 2 });
        this.htmlContent = markup("<h1>Markup Text</h1>");
        this.normalContent = "<h1>some content</h1>";
    }
    incrementSum() {
        this.state.sum++;
    }
}

