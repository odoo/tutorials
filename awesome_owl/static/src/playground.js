/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { TodoList, Counter, Card }

    setup() {
        this.state = useState({sum: 2})
    }

    incrementSum() {
        console.log('call')
        this.state.sum++
    }

    card_body = markup(`
        <span class="text-secondary">
            content of card <b>2</b>
        </span>
        `);
}

