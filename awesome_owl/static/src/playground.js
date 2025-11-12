/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { Card } from "@awesome_owl/Card/card";
import { TodoList } from "@awesome_owl/TodoList/todolist";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList};
    value1 = markup("<div>some text 1</div>");
    value2 = markup("<div>some text 2</div>");

    setup() {
        this.state = useState({ sum: 0 });
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum(value) {
        this.state.sum += value;
    }
}
