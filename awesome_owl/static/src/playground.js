/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./Todo/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  setup() {
    this.str1 = "<div class='text-uppercase'>Hello World</div>";
    this.str2 = markup("<div class='text-uppercase'>Hello World</div>");
    this.sum = useState({ value: 0 });
  }
  incrementSum() {
    this.sum.value++;
  }
  createInitialSum(value) {
    this.sum.value = this.sum.value + value;
  }
}
