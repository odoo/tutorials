import { Component, markup, useState } from "@odoo/owl";

import { Card } from "./card/card"
import { Counter } from "./counter/counter"
import { TodoList } from "./todo_list/todo_list"


export class Playground extends Component {
    static template = "my_module.Playground";
    static components = { Card, Counter, TodoList };

    value1 = "<div>some text 1</div>";
    value2 = markup("<div>some text 2</div>");

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
