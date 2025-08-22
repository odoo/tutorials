/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todoList";

export class Playground extends Component {

    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.html1 = '<b>Content of card 1</b>';
        this.html2 = markup('<b>Content of card 2</b>');
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
