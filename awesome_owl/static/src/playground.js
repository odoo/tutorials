/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";

import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.html = '<em>test</em>';
        this.test_html = markup(this.html);
        this.state = useState({ sum: 0 });
    }

    increment() {
        this.state.sum++;
    }
}
