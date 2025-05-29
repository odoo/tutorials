/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {
        Counter, Card
    };

    setup() {
        this.content1 = "<u>Card Content 1</u>";
        this.content2 = "<u>Card Content 2</u>";
        this.state = useState({ 
            sum: 0,
        });
    }

    incrementSum() {
        this.state.sum += 1;
    }
}
