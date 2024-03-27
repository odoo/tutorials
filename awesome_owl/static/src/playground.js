/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { TodoList, Counter, Card }

    state = useState({ sum: 0 });

    htmlContent = markup("<div>some content</div>")

    incrementSum() {
        this.state.sum++;
    }
}
