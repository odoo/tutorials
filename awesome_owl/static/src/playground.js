/** @odoo-module **/

import { useState, markup, Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};
    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum(value) {
        this.state.sum += 1;
    }
    content1 = "<div class='text-primary'>some content</div>"
    content2 = markup("<div class='text-primary'>some content</div>")
}
