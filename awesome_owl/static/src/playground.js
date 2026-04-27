import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = {Counter, Card, TodoList};
    static props = [];

    setup() {
        this.content1 = "<div class='text-primary'>some content</div>";
        this.content2 = markup("<div class='text-primary'>some content</div>");
        this.state = useState({sum: 0});
    }

    increment_total() {
        this.state.sum++;
    }
}
