import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoList } from "./components/todo_list/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  setup() {
    this.html_markup = markup("<div class='text-primary'>some content</div>");
    this.state = useState({ sum: 2 });
    this.incrementSum = this.incrementSum.bind(this);
  }

  incrementSum() {
    this.state.sum++;
  }
}
