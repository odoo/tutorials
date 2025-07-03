/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum(value) {
        this.state.sum += value;
    }

    content1 = "<div class='text-primary'>some content</div>"
    content2 = markup("<div class='text-primary'>some content</div>")
}
