import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoItem } from "./todo/todoitem";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoItem, TodoList };

    setup() {
        this.html = markup("<em style='color:red;'>Hello Red World</em>");
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }

}
