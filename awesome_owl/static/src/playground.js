/** @odoo-module **/

import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card};

    setup() {
        this.value1 = "<div class='text-danger'>Hello</div>";
        this.value2 = markup("<img src='x' onerror='alert(1)'/>");
        this.sum = useState({value: 2});
    }

    increment() {
        this.sum.value++;
    }
}
