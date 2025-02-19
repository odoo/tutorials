/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    setup() {
        this.heading_primar_esc = "<div class='text-success'>Heading</div>";
        this.heading_primar_markup = markup("<div class='text-success'>Heading</div>");
        this.sum = useState({ value: 0});
        this.incrementSum = this.incrementSum.bind(this)
    }

    incrementSum() {
        this.sum.value ++;
    }
}
