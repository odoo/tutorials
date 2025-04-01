/** @odoo-module **/

import { Component, markup, useState, xml } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./Todo/todoList";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = {
    Counter,
    Card,
    TodoList,
  };

  setup() {
    this.htmlContent1 = markup("<div>Hello <b>World</b></div>");
    this.htmlContent2 = markup(
      "<div class='text-primary'>Some italic content</div>"
    );
    this.state = useState({
      sum: 2,
    });
  }

  incrementSum(value) {
    this.state.sum++;
  }
}
