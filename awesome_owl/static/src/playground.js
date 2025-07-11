/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Card, Counter };

    // setup() {
    //     this.cards = [
    //         {
    //             title: "Plain Text Card",
    //             content: "This is a normal string. <i>This won't render as italic</i>",
    //         },
    //         {
    //             title: "HTML Card",
    //             content: markup("<i>This is <b>HTML</b> content</i>"),
    //         },
    //     ];
    // }

    // setup() {
    //     // This will store the total count of both counters
    //     this.state = useState({ sum: 0 });
    //     this.incrementSum = this.incrementSum.bind(this);
    // }

    // // This is the method that will be passed to children
    // incrementSum() {
    //     this.state.sum++;
    // }
}