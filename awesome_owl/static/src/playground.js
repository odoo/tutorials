/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    value1 = "<div class='text-primary'>some content</div>";
    value2 = markup("<div class='text-primary'>some content</div>");

    setup() {
        this.state = useState({ counters: {}, total: 0 });
    }

    update(index, value) {
        this.state.counters[index] = value;
        this.state.total = 0;

        Object.values(this.state.counters).forEach(counter => {
            this.state.total += counter;
        });
    }

}
