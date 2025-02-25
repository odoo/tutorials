import { Component} from "@odoo/owl";

export class DashboardItem extends Component{
    static template="awesome_dashboard.dashboardItem"
    static defaultProps = {
        size: 1,
      };
    static props=["text","size?"]
}
