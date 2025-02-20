/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todolist";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static props = [];
  static components = { Counter, Card, TodoList };
  html = markup("<div class='text-primary'>Some Content</div>");
  setup() {
    this.sum = useState({ value: 0 });
  }
  incrementSum() {
    this.sum.value++;
  }
}
