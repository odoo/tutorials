/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    value = markup("<a>lien giga bienveillant</div>");
    value2 = "<a href='enfer.com'>lien giga malfaisant</a>";

    setup() {
        this.state = useState({ sum: 0 });
    }

    increment() {
        this.state.sum++;
    }

    static components = { Counter, Card, TodoList };
}
