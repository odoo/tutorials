/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo_list/todo_list";
import { Card } from "./card/card";

export class Playground extends Component {}

Playground.components = { Counter, TodoList, Card }
Playground.template = "owl_playground.playground";