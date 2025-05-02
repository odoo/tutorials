import { Component, xml } from "@odoo/owl";
export class NumberCard extends Component {
  static template = xml`
    <div class="dashboard-card">
      <h3><t t-esc="props.title"/></h3>
      <p><t t-esc="props.value"/></p>
    </div>
  `;
}
