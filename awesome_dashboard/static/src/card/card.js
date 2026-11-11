import {Component, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "../dashboard_item/dashboard_item";
import {PieChart} from "../piechart/piechart";

export class Card extends Component {
    static template = "awesome_dashboard.Card";
    static components = {DashboardItem, PieChart};

    setup() {
        this.loadStatistics = useService("awesome_dashboard.statistics");
        this.statistics = {};
        onWillStart(async () => {
            this.statistics = await this.loadStatistics();
        })
    }
}