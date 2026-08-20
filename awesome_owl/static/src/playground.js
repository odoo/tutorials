import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };

  card1Content = '<div class="text-primary">some content 1</div>';
  card2Content = markup('<div class="text-primary">some content 2</div>');
}
