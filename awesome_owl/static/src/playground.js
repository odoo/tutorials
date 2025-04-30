import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./Card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter };
    setup(){
        this.onchange = this.onchange.bind(this);
        this.state = useState({
            value: markup("<div>some content</div>"),
            sum: 0
        });
    }
    
    onchange(){
        this.state.sum++;
    }
}
