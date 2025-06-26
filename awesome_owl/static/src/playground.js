/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todoList";
export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  setup() {
    this.state = useState({
      counter1: 0,
      counter2: 0,
    });
  }

  onCounter1Change(newValue) {
    this.state.counter1 = newValue;
  }

  onCounter2Change(newValue) {
    this.state.counter2 = newValue;
  }

  get sum() {
    return this.state.counter1 + this.state.counter2;
  }
}
