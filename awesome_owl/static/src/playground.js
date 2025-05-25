/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.str1 = markup("<strong>This is Card1 Content</strong>");
        this.str2 = "<em>This is Card2 Content</em>";
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
