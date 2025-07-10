/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.state = useState({ sum: 0 });
    }

    do_sum(value) {
        this.state.sum += value;
    }

    content1 = "<div>some content</div>";
    content2 = markup("<div class='text-primary'>some content</div>");

    static components = { Counter, Card, TodoList };
}
