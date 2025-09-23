/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.normal_string = "<div class='text-primary'>some content</div>";
        this.markup_string = markup("<div class='text-primary'>some content</div>");
        this.sum = useState({ value: 2 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
