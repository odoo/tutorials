import { Component, markup } from "@odoo/owl";
export class Card extends Component {
  static props = {
    title: String,
    content: String,
  };
  static template = "awesome_owl.Card";
}
