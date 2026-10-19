import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter,  Card };
    static props = [];

    setup() {
        this.htmlContent = markup`<div class="text-secondary">some content</div>`;
        this.state = useState({
            sum: 2,
        });
    }

    incrementSum() {
        this.state.sum++;
    }
}
