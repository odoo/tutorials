/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    content = markup("<div class='text-primary'>Full Stack Developer</div>");

    static components = { Counter, Card }

    setup() {
        this.state = useState({ sum: 2 });
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.state.sum++;
    }
}
