import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.html_content = markup("<h1>Markup Text</h1>");
        this.html_content2 = "<h1>Markup Text</h1>"
        this.sum = useState({ value: 2 })
    }

    incrementSum() {
        this.sum.value++;
    }
}
