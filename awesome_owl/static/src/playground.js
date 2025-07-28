/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";


export class Playground extends Component {
    static template = "awesome_owl.Playground";

    static components = { Counter, Card }
    html = '<button class="btn bg-warning">Test</button>'
    markup_html = markup(this.html)

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
