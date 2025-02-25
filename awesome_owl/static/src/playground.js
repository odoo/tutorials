/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };
  setup() {
    this.str1 = "<div class='text-uppercase'>Hello World</div>";
    this.str2 = markup("<div class='text-uppercase'>Hello World</div>");
  }
}
