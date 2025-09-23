/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};

    setup() {
        this.welcomeTxt = "Welcome to Monkey Town"
        this.content = "Save the monkeys"
        this.rawHtml = "<span style='color:red'>Raw HTML</span>"
        this.safeHtml = markup("<span style='color:green'>Medium Rare HTML</span>")
        this.counters = useState([
            { value: 0 },
            { value: 0 },
        ])
    }

    increment(index) {
        this.counters[index].value++
    }

    total() {
        return this.counters.reduce((a, b) => a + b.value, 0)
    }
}
