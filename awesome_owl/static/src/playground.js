/** @odoo-module **/

import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card}

    setup() {
        this.state = useState({
            sum: 2,
            value: "Awesome text",
            htmlValue: markup('<h1 class="font-italic">Hello</h1>')
        })
    }

    incrementSum() {
        this.state.sum++;
        console.log(this.state.sum)
    }
}
