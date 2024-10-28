/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static props = {};

    static template = "awesome_owl.playground";
    static components = { Card, TodoList };
}
