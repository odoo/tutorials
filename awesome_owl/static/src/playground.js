/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component
{
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList };

    setup()
    {
        this.sum = useState({ value: 2 });
    }

    incrementSum()
    {
        this.sum.value++;
    }
}
