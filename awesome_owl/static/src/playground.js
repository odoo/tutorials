/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup() {
        this.str1 = "<h1>Hello, World!</h1>";
        this.str2 = markup("<h1>Hello, World!</h1>");
        this.sum = useState( {count: 2});
    }

    incrementSum() {
        this.sum.count++;
    }
}


