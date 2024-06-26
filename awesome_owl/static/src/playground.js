/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card";
import { Counter } from "./counter";
import { TodoList } from "./todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.value1 = markup("<div>some</div><div> text</div><div>.</div>");
        this.value2 = markup("<h5>some other text 2</h5>");
        this.sum = useState({ value: 2 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
