import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = []

    setup() {
        this.html = markup("<i>some content rendered from html</i>");
        this.state = useState({ sum: 0});
    }

    incrementSum() {
        console.log("incrementSum called")
        this.state.sum++;
    }
}
