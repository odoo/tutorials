/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };
  value1 = "<div>Normal string</div>";
  value2 = markup("<b>Markup string</b>");

  setup() {
    this.sum = useState({ value: 0 });
  }

  sumofCounter() {
    this.sum.value++;
  }
}
