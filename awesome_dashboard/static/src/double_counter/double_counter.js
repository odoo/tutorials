import { Component, xml, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DoubleCounter extends Component {
  static template = xml`
    <t t-esc="'selected: ' + state.selected + ', value: ' + service.state[state.selected]"/>
    <button t-on-click="() => service.increment('count1')">increment count 1</button>
    <button t-on-click="() => service.increment('count2')">increment count 2</button>
    <button t-on-click="changeCounter">Switch counter</button>
  `;
    setup() {
      this.state = useState({ selected: "count1" });
      this.service = useService("double_counter");
    }
  changeCounter() {
    this.state.selected = this.state.selected === "count1" ? "count2" : "count1";
  }
}