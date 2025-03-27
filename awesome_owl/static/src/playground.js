/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { CounterComponent } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  setup() {
    this.sum = useState({ value: 2 });
    this.str1 = "<div class='text-primary'>content</div>";
    this.str2 = markup("<div class='text-primary'>content</div>");
  }
  incrementSum() {
    this.sum.value++;
  }
  static components = { CounterComponent, Card, TodoList };
}
