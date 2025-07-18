/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { Card } from "@awesome_owl/card/card";
import { TodoList } from "@awesome_owl/todo_list/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  setup() {
    this.state = useState({
      sum: 2,
    });

    this.counterValues = [1, 1];
  }
  updateCounterValue(index, newValue) {
    this.counterValues[index] = newValue;
    this.state.sum = this.counterValues.reduce((a, b) => a + b, 0);
  }

  handleCounterChange = (index) => {
    return (val) => this.updateCounterValue(index, val);
  };
}
