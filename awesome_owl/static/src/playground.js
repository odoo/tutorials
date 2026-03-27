import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = []

    value1 = "<div>some text 1</div>";
    value2 = markup("<div>some text 2 using markup</div>");

    setup() {
        this.sum = useState({ value: 2 });
    }

    incrementSum() {
        this.sum.value++
    }
}
