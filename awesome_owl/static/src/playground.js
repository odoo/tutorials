/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { ToDoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    titlevalue = markup("<div>Card 1</div>");
    titlevalue2 = markup("<div>Card 2</div>");

    incrementSum() {
        this.sum.value++;
    }
    decrementSum() {
        this.sum.value--;
    }

    sum = useState({ value: 2 })

    static components = { Counter, Card, ToDoList };
}   
