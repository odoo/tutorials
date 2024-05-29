/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/Counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };
  setup() {
    this.str1 = "<div class='text-primary'>some content</div>";
    this.str2 = markup("<div class='text-primary'>some content</div>");
    this.sum = useState({ value: 2 });
  }
  incrementSum() {
    this.sum.value++;
  }
}
