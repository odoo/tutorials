/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.content_1 = "<div class='text-primary'>some content</div>";
        this.content_2 = markup("<div class='text-primary'>some content</div>");
        this.counter = useState({ value:[{id:0,value:1},{id:1,value:1}] });
    }

    incrementCounter(index) {
        this.counter.value[index].value++;
    }

    get counterSum() {
        return this.counter.value.reduce((acc, val) => acc + val.value, 0);
    }

    static components = { Counter, Card };
}
