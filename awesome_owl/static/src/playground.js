/** @odoo-module **/
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";

import { Component, useState, markup } from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    content1 = "<div class='text-primary'>some text 1</div>";
    content2 = markup("<div class='text-primary'>some text 2</div>");

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
