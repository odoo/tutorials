import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./card/card.js";
import { TodoList } from "./todo/todo.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList }

    setup() {
        this.total = useState({ sum:2 });
        this.state = useState({
            htmlContent: markup("<b>This is bold text</b>")
        });
    }

    incrementSum(value) {
        this.total.sum += value;
    }
}
