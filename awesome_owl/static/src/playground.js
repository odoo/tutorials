/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { TodoList };

}