/** @odoo-module **/

import { Component } from "@odoo/owl";
import { ToDoList } from "./todolist/todolist";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, ToDoList };
}
