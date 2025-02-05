import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.dashboarditem";
    static props ={
        size: { type: Number, optional: true, default: 1},
        }

}