/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { useClicker } from "../clicker_hook";

export class ClickerValue extends Component {
  static template = xml`
    <t t-name="awesome_clicker.clicker_value">
        <span t-att-data-tooltip="this.clicker.count" t-esc="formatedCount()"/>
    </t>
    `;

  setup() {
    this.clicker = useClicker();
  }

  formatedCount = () => {
    const count = this.clicker.count;

    return count.toString().length > 3
      ? humanNumber(count, { decimals: 1 })
      : count;
  };
}

registry.category("actions").add("awesome_clicker.clicker_value", ClickerValue);
