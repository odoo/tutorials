/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";

// Custom elements
import { Card } from "./card/card";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Card, Counter };

    setup() {
        this.card_contents = [
            { title: "Title 1", content: "<div>Text content 1</div>" },
            { title: "Title 2", content: markup("<div>Text content 2</div>") }
        ];

        this.state = useState({ total: 2});
    }

    incrementSum() {
        this.state.total++;
    }
}
