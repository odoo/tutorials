/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card };

    setup() {
        this.cards = [
            { title: "Safe String", content: "This is a normal string" },
            { title: "Styled HTML", content: markup("<b style='color: red;'>This is bold and red</b>") },
            { title: "List Example", content: markup("<ul><li>Item 1</li><li>Item 2</li></ul>") },
        ];
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
