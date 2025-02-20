/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from './counter/counter';
import { Card } from './card/card';
import { TodoList } from './todo/todo_list';

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    content1 = "<a href='https://google.com'>google</a>";
    content2 = markup("<a href='https://google.com'>google</a>");
    state = useState({ sum: 2 });

    incrementSum() {
        this.state.sum++;
    }
}
