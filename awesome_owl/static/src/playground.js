/** @odoo-module **/

import { Component, markup , useState} from "@odoo/owl";
// import { Counter } from "./counter/counter";
import { Card } from "./card/card.js";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {
        // Counter: Counter,
        Card: Card,
    }

    setup() {
        this.html1 = `<h3>some content</h3>`
        this.html2 = markup`<h3>some more content</h3>`
    }
}
