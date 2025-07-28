/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };

  setup() {
    this.regularHtml = "<div class='text-danger'>This will be escaped</div>";
    this.safeHtml = markup(
      "<div class='text-primary'>This will render as HTML</div>"
    );
    this.markup = markup;
  }
}
