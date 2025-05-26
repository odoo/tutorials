/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    
    setup() {
        this.someHTML = markup("<div class='text-primary'>some content</div>");
        this.someText = "<div class='text-primary'>some content</div>";
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
