/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = { Counter, Card };

  setup() {
    this.sum = useState({ value: 2 });
    this.incrementSum = this.incrementSum.bind(this);

    this.content1 = "<p>This is <b>bold</b></p>";
    this.content2 = markup("<p>This is <b>bold</b></p>");
  }

  incrementSum() {
    this.sum.value++;
  }
}
