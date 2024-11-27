import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static props = {};

  setup() {
    this.state = useState({ sum: 0 });
  }

  incrementSum() {
    this.state.sum++;
  }

  content1 = "<div class='text-primary'>some content</div>";
  content2 = markup(this.content1);

  static components = { Counter, Card, TodoList, Playground };
}
