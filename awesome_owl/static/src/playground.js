/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";

import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.title_test_1 = "Test 1";
        this.content_test_1 = markup("<div class='text-primary'>Html content yay</div>");
        
        this.state = useState({ sum : 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
