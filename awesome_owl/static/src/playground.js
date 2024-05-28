/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TodoList } from "./todo_list/todo_list";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { TodoList, Card, Counter };

}