/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card"

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card };
    value1 = "<div class='text-primary'>some text 1</div>";
    value2 = markup("<div class='text-primary'>some text 2</div>");

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
