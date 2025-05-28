import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.s1 = "<div class='text-primary'>some content</div>";
        this.s2 = markup("<div class='text-primary'>some content</div>");
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
