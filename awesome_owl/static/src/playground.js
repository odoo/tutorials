/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Card, Counter, TodoList};
    markupText = markup("<div class='text-primary'>some content</div>");

    setup() {
        this.state = useState({sum: 0});
    }

    incrementSum() {
        this.state.sum++;
    }
}
