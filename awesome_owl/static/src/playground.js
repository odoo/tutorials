import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./Card/card";
import { markup } from "@odoo/owl";
import { TodoList } from "./TodoList/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }

    // setup() {
    //     this.safeHtml = markup("<strong>This is bold content.</strong>");
    //     this.unsafeHtml = "<em>This will be escaped and not rendered as HTML.</em>";
    //   }
}

