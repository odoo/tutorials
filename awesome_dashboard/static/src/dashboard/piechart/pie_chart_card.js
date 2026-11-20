import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { PieChart } from "./piechart";

export class PieChartCard extends Component {
  static template = "awesome_dashboard.PieChartCard";
  static components = { PieChart };
  static props = {
    title: { type: String },
    data: { type: Object, optional: true },
  };
  static defaultProps = {
    data: {},
  };
  get translatedTitle() {
    return _t(this.props.title);
  }
}
