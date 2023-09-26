/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from './counter/counter'
import { Card } from './card/card'
import { TodoList } from './todo_list/todo_list'

export class Playground extends Component {
}

Playground.template = "owl_playground.playground";
Playground.components = { Counter, TodoList, Card }
