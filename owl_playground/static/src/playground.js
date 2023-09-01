/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { TodoList } from "./Todo-list/todo-list";
import { Card } from "./Card/card";

export class Playground extends Component {
  static template = "owl_playground.playground";
  static components = { Counter, TodoList, Card };
  setup() {
    this.todo = { id: 3, description: "buy milk", done: false };
  }
}
