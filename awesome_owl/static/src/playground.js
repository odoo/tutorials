/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.content = "<div>some content</div>";
        this.content2 = markup("<div>some content</div>");
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
