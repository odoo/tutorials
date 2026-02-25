import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadStatistics } from "@awesome_dashboard/services/statistics_service";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, PieChart };

    setup() {
        this.action = useService("action");

        this.state = useState({
            stats: null,
        });

        onWillStart(async () => {
            this.state.stats = await loadStatistics();
        });
    }
}