import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "../counter/counter"
import { Card } from "../card/card";
import { TodoList } from "../todo/todolist";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = { Counter, Card, TodoList };

  setup() {
    this.state = useState({ sum: 0 });
    this.text1 = markup("<div class='text-primary fs-5' > text1 </div>");
  }

  incrementSum() {
    this.state.sum++;
  }
}
