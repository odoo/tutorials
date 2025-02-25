/** @odoo-module **/

import { Component } from "@odoo/owl";
import { ToDoList } from "./todolist/todolist";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { ToDoList };
}
