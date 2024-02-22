/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = { Counter, Card };

  setup() {
    this.content1 = "<p>This is <b>bold</b></p>";
    this.content2 = markup("<p>This is <b>bold</b></p>");
  }
}
