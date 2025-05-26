/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    someHTML = markup("<div class='text-primary'>some content</div>")
    someText = "<div class='text-primary'>some content</div>"

    setup() {
        this.state = useState({ value:0});
    }
    
    increment() {
        this.state.value++;
    }
}
