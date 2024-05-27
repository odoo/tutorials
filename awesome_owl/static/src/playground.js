/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    content1 = "<div class='p-3'>my content is so cool</div>"
    content2 = markup("<div class='p-3 text-primary'>my content is so cool</div>")

    setup() {
        this.state = useState({
            sum: 0
        })
    }

    incrementSum() {
        this.state.sum ++;
    }
}
