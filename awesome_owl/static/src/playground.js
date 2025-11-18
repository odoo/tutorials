import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    nonescaped_html = "<div>some content</div>";
    escaped_html = markup("<div>some content</div>");

    setup() {
        this.incrementSum = this.incrementSum.bind(this);
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
