/** @odoo-module **/
import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };
  static props = {};

  value = markup("<div class='text-primary'>some text</div>");

  setup() {
    this.state = useState({ sum: 0 });
    // this.incrementSum = this.incrementSum.bind(this);
  }

  incrementSum() {
    this.state.sum++;
  }
}
