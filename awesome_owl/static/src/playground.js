import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    someHtml = "<div class='text-primary'>some content</div>"
    markupedHtml = markup(this.someHtml);

    static components = {
        Counter,
        Card,
        TodoList
    };

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
