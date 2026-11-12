import {Component} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "../dashboard_item/dashboard_item";

export class Card extends Component {
    static template = "awesome_dashboard.Card";
    static components = {DashboardItem};
    static props = {
        items: Array,
    };

    setup() {
        this.statistics = useService("awesome_dashboard.statistics");
    }
}