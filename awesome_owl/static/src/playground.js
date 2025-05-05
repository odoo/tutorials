import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todolist/todolist";

export class Playground extends Component {
    static components = { Counter, Card, TodoList };

    static template = "awesome_owl.playground";

    static props = {};

    html1 = '<div style="background-color: red">some content</div>';
    html2 = markup('<div style="background-color: red">some content</div>');

    setup() {
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
