import { Component } from "@odoo/owl";

export class DashboardItemContent extends Component {
    static template = 'awesome_dashboard.dashboard_item_content'
    static props = {
        text: String | Number
    }
}