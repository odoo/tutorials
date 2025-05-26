/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {
        Counter,
        Card,
        TodoList
    };
    setup() {
        this.sum = useState({ value: 2 });
        this.sampleHtml ="<div><strong>this is a test</strong></div>";
    }
    
    get markupValue() {
        return markup(this.sampleHtml);
    }

    incrementSum() {
        this.sum.value++;
    }
}
