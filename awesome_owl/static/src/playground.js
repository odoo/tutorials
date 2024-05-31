/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.str1 = markup("<div> some content</div>");
        this.sum = useState({ value: 0})
    }

    increment(){
        this.sum.value++;
    }
}
