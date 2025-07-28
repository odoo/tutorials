import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo-list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  setup() {
    this.regularHtml = "<div class='text-danger'>This will be escaped</div>";
    this.safeHtml = markup(
      "<div class='text-primary'>This will render as HTML</div>"
    );

    this.markup = markup;

    this.state = useState({ sum: 0 });
  }

  incrementSum() {
    this.state.sum += 1;
  }
}
