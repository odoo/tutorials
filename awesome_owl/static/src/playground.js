/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
  static components = { Counter, Card, TodoList};
  static template = "awesome_owl.playground";

  setup() {
    this.cards = [
      {
        title: "Card 1",
        text: "<div>This is <b>bold</b></div>", 
      },
      {
        title: "Card 2",
        text: markup("<div>This is <b>bold</b></div>"),
      },
    ];

    this.state = useState({
      sum: 2,
    });
  }

 
  incrementSum() {
    this.state.sum +=1 
    }
}
