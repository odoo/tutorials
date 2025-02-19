/** @odoo-module **/

import { Component, useState, markup} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    static props = {}

    setup() {
        this.card1Description = "some content";
        this.card2Description = markup("<div>some contentss</div>");

        this.sum = useState({ value: 2 });
        this.incrementSum = () => {
            this.sum.value++;
        }
    }
}
