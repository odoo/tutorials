/** @odoo-module **/

import { Component } from "@odoo/owl";
import { DashboardItem } from "../dashboard_item/dashboard_item";


export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";
    static components = { DashboardItem }
}