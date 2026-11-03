import { Component, t, useProps }  from "@odoo/owl";
import { DashboardItem } from "../dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
    static template = 'awesome_dashboard.PieChartCard';
    static components = { DashboardItem, PieChart };

    props = useProps({
        title: t.string(),
        values: t.array(),
        labels: t.array(),
    });
}

export default PieChartCard;
