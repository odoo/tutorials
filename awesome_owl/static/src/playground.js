/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo_list";
import { TodoItem } from "./todo/todo_item";


export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList, TodoItem };

  setup() {
    this.safeHtml = markup("<div>some <b>bold </b>text</div>");
    this.normalText = "<div>some text 1</div>";
    this.sum = useState({ value: 0 });
  }
  incrementSum() {
    this.sum.value++;
  }
}
