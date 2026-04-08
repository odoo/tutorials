import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card"
import { TodoList } from "./Todo/TodoList/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.str1 = markup("<div>some content</div>");
        this.str2 = "<div>some content</div>";
        this.sum = useState({ value: 2 })
    }

    incrimentSum() {
        this.sum.value++;
    }
    decrimentSum() {
        this.sum.value--;
    }

    static components = { Counter, Card, TodoList }
}
