import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
    static props = []

    setup() {
        this.html = markup("<i>some content rendered from html</i>");
        this.state = useState({ sum: 0});
    }

    incrementSum() {
        console.log("incrementSum called")
        this.state.sum++;
    }
}
