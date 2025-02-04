/** @odoo-module **/

import { Component, useState,markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    sum = useState({ value: 2 });

    incrementsum=()=> {
        this.sum.value++; 
    }

    name2 = markup("<div style='color:blue;'>Some Text 2</div>");
}
