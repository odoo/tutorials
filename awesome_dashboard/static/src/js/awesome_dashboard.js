import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { statisticsStore } from "@awesome_dashboard/services/statistics_service";
import { DashboardItem } from "../js/dashboard_item";
import { PieChart } from "../js/pie_chart";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, PieChart };

    setup() {
        this.action = useService("action");

        this.stats = useState(statisticsStore);
    }
}