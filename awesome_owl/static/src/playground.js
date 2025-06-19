/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todoList/todoList";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  setup() {
    this.sum = useState({ value: 0 });
  }

  sumofCounter() {
    this.sum.value++;
  }
}
