/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };
  static props = {};

  setup() {
    this.state = useState({ sum: 0 });
  }
  
  card1ContentValue = markup("<div class='text-primary'>Some Content</div>");

  incrementSum() {
    this.state.sum += 1;
  }
}
