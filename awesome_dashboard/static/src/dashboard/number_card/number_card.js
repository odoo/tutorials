import { Component } from "@odoo/owl";
import { DashboardItem } from "../dashboard_item/dashboard_tem";

export class NumberCard extends Component {
    static template = "awesome_dashboard.number_card";
    static components = { DashboardItem }
    static props = {
        size: {
            type: Number,
            optional: true
        },
        data: Number,
        description: Number,
    }
}
