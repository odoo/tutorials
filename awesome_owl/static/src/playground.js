/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList }

    setup() {
        this.content1 = '<div class="text-primary">Content of Card 1</div>';
        this.content2 = markup('<div class="text-primary">Content of Card 2</div>');

        this.sum = useState({ value: 2 });
    }

    onChange() {
        this.sum.value++;
    }
}
