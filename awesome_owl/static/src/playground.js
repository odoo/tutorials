/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Card, Counter, TodoList };

  setup() {
    this.plainText = "<div><strong>Plain text content</strong></div>";
    this.htmlContent = markup("<div><strong>Markup content</strong></div>");
    this.state = useState({
      counter1: 0,
      counter2: 0,
    });
    this.incrementSum = (counterNumber, newValue) => {
      this.state[counterNumber] = newValue;
    };
  }

  get sum() {
    return this.state.counter1 + this.state.counter2;
  }
}
