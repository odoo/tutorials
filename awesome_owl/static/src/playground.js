/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";
import { TodoItem } from "./todo/todo_item";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList, TodoItem };

  setup() {
    this.sum = useState({ value: 0 });
  }
  increment() {
    this.sum.value++;
  }
}
