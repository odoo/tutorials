/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";

import { Counter } from "./counter/counter.js"
import { Card } from "./card/card.js"
import { TodoList } from "./todo/todo_list.js"

export class Playground extends Component {

    static template = "my_module.Playground";
    static components = { Counter, Card, TodoList };

    card_content = markup("<a href=''>some content</a>");

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum(){
        this.state.sum++;
    }
}
