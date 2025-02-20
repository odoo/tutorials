/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { CounterComponent } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  setup() {
    this.state = useState({ value: 4 });
  }
  increment() {
    this.state.value++;
  }

  static components = { CounterComponent, Card }
}
