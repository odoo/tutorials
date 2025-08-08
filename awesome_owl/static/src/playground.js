/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    html = markup("<div class='text-primary'>some content</div>");

    sum = useState({ value: 2});

    incrementSum() {
        this.sum.value++;
    }

    static props = {};
}
