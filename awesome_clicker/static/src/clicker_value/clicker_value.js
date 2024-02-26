/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { useClicker } from "../clicker_hook";

export class ClickerValue extends Component {
  static template = xml`
    <t t-name="awesome_clicker.clicker_value">
        <t t-esc="formatedCount()"/>
    </t>
    `;

  setup() {
    this.clicker = useClicker();
  }

  formatedCount = () => humanNumber(this.clicker.state.count);
}

registry.category("actions").add("awesome_clicker.clicker_value", ClickerValue);
