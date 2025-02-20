import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground_template";
    static props = {};
    setup() {
        this.htmlContent = markup("<div><strong>This is bold text inside a div.</strong></div>");
        this.plainText = "This is normal text";
        this.state = useState({ counter1: 2});
    }

    static components = { Counter, Card };

    updateCounter1() {
        this.state.counter1 += 1;
    }
}

