import { Component } from "@odoo/owl";

export class DashboardItem extends Component{
    static template = "awesome_dashboard.AwesomeDashboardItem";
    static defaultProps = {
        size: 1,
    }; 
}
