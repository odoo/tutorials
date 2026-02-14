import { Component } from "@odoo/owl";
import { DashboardItem } from "../DashboardItem/dashboardItem";


export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static components = { DashboardItem };
}
