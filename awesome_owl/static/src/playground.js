import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({c1: 0, c2: 0});
        this.str1 = markup("<div class='text-primary'>some content</div>");
    }

    updateC1(value) { this.state.c1 = value; }
    updateC2(value) { this.state.c2 = value; }
}
