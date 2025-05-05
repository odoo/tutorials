import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 0 });
        this.html = "<div>some text</div>";
        this.html_markup = markup("<div>some text using markup</div>");
    }

    incrementSum() {
        this.sum.value++;
    }
}
