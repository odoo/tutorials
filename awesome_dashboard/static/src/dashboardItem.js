import { Component } from "@odoo/owl";

export class DashboardItem extends Component{
    static template = "awesome_dashboard.dashboardItem";
    static props =  {
        size : {type:Number, optional: true, default:1},
    };
}