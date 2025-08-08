/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter"
import { Card } from "./components/card/card"
import { ToDoList } from "./components/TodoList/todolist"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, ToDoList};
    setup() {
        this.state = useState({
            sum: 2
        });
    };

    incrementSum(){
        this.state.sum++;
    }

    content1= "<div>Card with no markup</div>";
    content2 = markup("<div>Card with markup content</div>");
}
