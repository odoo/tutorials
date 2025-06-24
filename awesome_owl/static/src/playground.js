/** @odoo-module **/

import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todoList";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    setup() {
        this.markupValue = markup("<div>MarkUP text</div>");
        this.state = useState({ sum: 0 });
    }

    increment(){
        this.state.sum ++;
    }

    static components = { Counter, Card, TodoList };
}