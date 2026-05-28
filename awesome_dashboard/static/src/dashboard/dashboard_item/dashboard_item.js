import { Component } from '@odoo/owl';

export class DashboardItem extends Component {
  static template = 'awesome_dashboard.dashboard_item';

  static props = {
    slots: { type: Object, optional: true },
    size: { type: Number, optional: true, default: 1 },
  };

  get itemSize() {
    return this.props.size ?? 1;
  }
}
