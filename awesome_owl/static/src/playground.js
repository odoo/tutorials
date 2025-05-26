/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.title = "[Odoo] New version here!!!";
        this.content = markup("<div><span>19.0</span></div>");
        this.sum = useState({value: 0});
    }

    incrementSum() {
        this.sum.value++;
    }
}
