import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todoList/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    value2 = markup("<a href='http://odoo.com'>Test</a>");

    setup() {
        this.total = useState({ value: 0 });
    }

    incrementSum() {
        console.log("aaa")
        this.total.value++;
    }

    static components = { Counter, Card, TodoList };
}
