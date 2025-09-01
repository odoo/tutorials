/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList }

    setup() {
        this.headingPrimaryEsc = "<div class='text-success'>Heading</div>";
        this.headingPrimaryMarkup = markup("<div class='text-success'>Heading</div>");
        this.sum = useState({ value: 0});
        this.incrementSum = this.incrementSum.bind(this)
    }

    incrementSum() {
        this.sum.value ++;
    }
}
