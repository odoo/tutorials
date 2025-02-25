/** @odoo-module **/

import { Component, markup, useState } from '@odoo/owl';
import { Counter } from './counter/counter';
import { Card } from './card/card';
import { TodoList } from './todolist/todo_list';

export class Playground extends Component {
    static template = 'awesome_owl.playground';
    static components = { Counter, Card, TodoList };
    static props = {};

    setup() {
        this.escapedValue = 'Hello, <b>world</b>!';
        this.notEscapedValue = markup('Hello, <b>world</b>!');
        this.countersSum = useState({
            value: 0,
        });
        this.increaseSum = this.increaseSum.bind(this);
    }

    increaseSum() {
        this.countersSum.value++;
    }
}
