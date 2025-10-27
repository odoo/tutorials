/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from './counter/counter';
import { Card } from './card/card';
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        this.sum = useState({ value: 0 });
    }

    title1 = 'Title 1';
    title2 = 'Title 2';

    content1 = "<div>Some content</div>";
    content2 = markup("<div>Some content</div>");

    incrementSum() {
        this.sum.value++;
    }

}
