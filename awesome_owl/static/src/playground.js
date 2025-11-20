/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoItem } from "./todo_item/todo_item";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  setup() {
    this.sum = useState({ value: 2 });
    this.str1 = "<div class='text-primary'>content</div>";
    this.str2 = markup("<div class='text-primary'>content</div>");
  }
  incrementSum() {
    this.sum.value++;
  }
  static components = { Counter, Card , TodoList , TodoItem};
}
