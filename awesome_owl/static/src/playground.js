/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./card/card.js"
import { TodoList } from "./todo/todo_list.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.state = {
            title: "My title",
            safeHtml: markup("<div style='color:red'>This is <b>HTML</b> content</div>"),
            unsafeHtml: "<div style='color:red'>This will be escaped</div>",
        }
        this.sum = useState({ value: 0 });
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.sum.value += 1;
    }
}
