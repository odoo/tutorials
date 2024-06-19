/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
  static props = [];
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  setup() {
    this.state = useState({ sum: 2 });
  }

  incrementSum() {
    this.state.sum++;
  }
}
