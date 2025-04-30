import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup(){
        this.state = useState({ title: "string", content: "string" });
        this.html_value_1 = "<div>some text 1</div>";
        this.html_value_2 = markup("<div>some text 2</div>");
        this.sum = useState({ value: 3 })
    }

    incrementSum(){
        this.sum.value++;
    }
}
