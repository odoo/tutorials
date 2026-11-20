import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo_list/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Card, Counter, TodoList };

  setup() {
    this.html = markup("<p>This is some content</p>");
    this.html2 = "<p>This is some content</p>";
    this.sum = useState({ value: 0 });
  }
  incrementSum(increment) {
    if (increment) {
      this.sum.value++;
    } else {
      this.sum.value--;
    }
  }
}
