/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./Card/card.js";
import { TodoList } from "./todo/todo_list.js";

const html = "<div class='text-primary'>some content</div>";
export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };
  setup() {
    this.state = useState({ sum: 2 });
    this.incrementSum = (newValue) => {
      this.state.sum++;
    };
    this.card1 = {
      title: "card 1",
      content: markup(html),
    };
    this.card2 = {
      title: "card 2",
      content: markup("<b>another content</b>"),
    };
  }
}
