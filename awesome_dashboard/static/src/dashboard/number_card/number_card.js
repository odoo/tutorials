/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
  static template = xml`<div class="o_number_card">
        <h3 t-esc="props.title"/>
        <p class="o_number" t-esc="props.value"/>
    </div>`;

  setup() {
    this.defaultProps = {
      size: 1,
    };
  }

  static props = {
    value: String,
    title: String,
  };
}
