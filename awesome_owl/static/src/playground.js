import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template =  "awesome_owl.Playground";
    static components = { Counter, Card, TodoList}

    setup() {
        this.normalHtml = "<div class='text-primary'>some content</div>";

        this.safeHtml = markup("<div class='text-primary'>some content</div>");

        this.state = useState({ sum: 0 });
    }
    incrementSum() {
        this.state.sum++;
    }
}
