import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };

  setup() {
    this.htmlContent = markup("This is <b>bold</b> and <i>italic</i> text!");
  }
}
