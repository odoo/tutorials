/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Todo } from "./todo/todo";
import {Todolist} from "./todolist/todolist";
import { Card } from "./card/card";
export class Playground extends Component {
    static components = { Counter,Todo,Todolist,Card };
    static template = "owl_playground.playground";

    setup() {
        this.todo = { id: 3, description: "buy milk", done: true };

    }
}

