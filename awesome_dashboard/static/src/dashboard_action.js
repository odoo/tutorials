import { Component,xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

export class DashboardLazyLoader extends Component {
  static template = xml`
  <LazyComponent bundle="'awesome_dashboard.dashboard_assests'" Component="'AwesomeDashboard'"/>
  `;
  static components = { LazyComponent };
  
}
registry
  .category("actions")
  .add("awesome_dashboard.dashboard_action", DashboardLazyLoader);
