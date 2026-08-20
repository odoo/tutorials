import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };

  state = useState({ value: 0 });

  card1Content = '<div class="text-primary">some content 1</div>';
  card2Content = markup('<div class="text-primary">some content 2</div>');

  incrementSum() {
    this.state.value++;
  }
}
