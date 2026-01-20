import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./Todo/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };
  static props = [];

  setup() {
    this.state = useState({
      sum: 0,
    });
  }

  incrementSum = () => {
    this.state.sum++;
  };

  toggle = () => {
    this.state.isOpen = !this.state.isOpen;
  };

  htmlString = "<div style='color: red'>This is red text</div>";
  safeHtmlString = markup("<div style='color: green'>This is green text</div>");
}
