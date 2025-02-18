import { Component, markup } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };

  setup() {
    this.html_markup = markup("<div class='text-primary'>some content</div>");
  }
}
