import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";
import { TodoItem } from "./todo_item/todo_item";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList };

    setup() {
        super.setup();

        this.state = useState({
            html: "<i>my html content</i>" ,
            html2: markup("<i>my html content</i>"),
            counter1: 0,
            counter2: 0,
        });

        this.increment1 = this.increment1.bind(this);
        this.increment2 = this.increment2.bind(this);
    }

    increment1(value) {
        this.state.counter1 = value;
    }

    increment2(value) {
        this.state.counter2 = value
    }
}
