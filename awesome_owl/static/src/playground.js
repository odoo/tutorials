/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from './Counter/counter';
import { Card } from './Card/card';
import { TodoList } from "./ToDo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { TodoList, Card, Counter };

    html = markup("<div>some content</div>")
    counters_sum = useState({ value: 0 });

    incrementSum() {
        this.counters_sum.value++;
    }
}
