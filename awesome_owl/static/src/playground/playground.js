/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";
import { Card } from "../card/card";
import { TodoList } from "../todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.state = useState({ value: 0 });
        this.contentCard1 = "<div>content card 1</div>";
        this.contentCard2 = markup("<div>content card 2</div>");
    }

    incrementSum() {
        this.state.value++;
    }
}
