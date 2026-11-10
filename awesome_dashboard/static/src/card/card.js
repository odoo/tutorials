import {Component} from "@odoo/owl";
import {DashboardItem} from "../dashboard_item/dashboard_item";

export class Card extends Component {
    static template = "awesome_dashboard.Card";
    static components = {DashboardItem};
}