import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.state = useState({ sum: 2 });
        this.html1 = "<div>some content</div>";
        this.html2 = markup("<div>some content</div>");
    }

    incrementSum() {
        this.state.sum++;
    }
}
