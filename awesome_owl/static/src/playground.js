import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup(){
        this.htmlContent = markup("<span style='color:blue; font-weight:700'>some content.</span>")
        this.normalString = "<p style='color:blue>some content.</p>"
        this.state = useState({ sum: 0 });
    }

    incrementSum(){
        this.state.sum++;
    }
}
