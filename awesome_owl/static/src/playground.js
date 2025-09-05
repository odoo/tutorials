/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }
    setup() {
        this.value1 = "<div>some text 1</div>";
        this.value2 = markup("<div>some text 2</div>");
        this.sum = useState({ value: 2 })
    }
    incrementSum() {
        this.sum.value = this.sum.value + 1;
    }
}
