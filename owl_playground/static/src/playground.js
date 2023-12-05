/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo";

export class Playground extends Component {
    static template = "owl_playground.playground";
    static components = { Counter, TodoList };
}
