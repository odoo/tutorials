/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    setup() {
        this.card1_body = "<div class='text-primary'>some content</div>";
        this.card2_body = markup("<div class='text-primary'>some content</div>");
        this.sum = useState({ value: 0 });
    }

    onIncrement() {
        this.sum.value++;
    }
    static components = { Counter, Card };
}
