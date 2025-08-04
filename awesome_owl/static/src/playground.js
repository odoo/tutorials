/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    content1 = "<div style=\"color:blue\">this is outside a markup</div>"
    content2 = markup("<div style=\"color:blue\">this is inside a markup</div>");

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum()
    {
        this.state.sum++;
    }
}
