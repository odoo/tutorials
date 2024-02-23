/** @odoo-module */

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
  static template = xml`
  <t t-name="awesome_dashboard.NumberCard" owl="1">
    <t t-esc="props.title"/>
    <div class="fs-1 fw-bold text-success text-center">
        <t t-esc="props.value"/>
    </div>
  </t>`;
  
  static props = {
    title: {
      type: String,
    },
    value: {
      type: Number,
    },
  };
}
