import { Component, xml, useState } from "@odoo/owl";

export class DoubleCounter extends Component {
  static template = xml`
    <t t-esc="'selected: ' + state.selected + ', value: ' + state[state.selected]"/>
    <button t-on-click="() => this.state.count1++">increment count 1</button>
    <button t-on-click="() => this.state.count2++">increment count 2</button>
    <button t-on-click="changeCounter">Switch counter</button>
  `;

  setup() {
    this.state = useState({ selected: "count1", count1: 0, count2: 0 });
  }

  changeCounter() {
    this.state.selected = this.state.selected === "count1" ? "count2" : "count1";
  }
}