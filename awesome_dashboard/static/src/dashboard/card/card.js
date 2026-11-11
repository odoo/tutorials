import {Component} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "../dashboard_item/dashboard_item";
import {registry} from "@web/core/registry";

export class Card extends Component {
    static template = "awesome_dashboard.Card";
    static components = {DashboardItem};

    setup() {
        this.statistics = useService("awesome_dashboard.statistics");
        this.items = registry.category("awesome_dashboard").getAll();
    }
}