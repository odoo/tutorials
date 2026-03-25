import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList };

    setup() {
        this.state = useState({ sum: 2 });
    }

    value1 = "<div class='text-primary'>some text 1</div>";
    value2 = markup("<div class='text-primary'>some text 2</div>");

    incrementSum() {
        this.state.sum++;
    }
}
