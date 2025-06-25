import { Component, onWillStart, useRef, useEffect, onWillUnmount, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChartTemplate";
    static props = {
        label: { type: String },
        data: { type: Object }
    }
    setup() {
        this.chartRef = useRef("chartCanvas");
        this.chart = null;
        this.statistics = useState(useService("awesome_dashboard.statistics"));

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(() => {
            this.renderChart();
        });
        
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        if (this.chart) this.chart.destroy();
        this.chart = new Chart(this.chartRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.statistics.data.orders_by_size),
                datasets: [{
                    label: this.props.label,
                    data: Object.values(this.statistics.data.orders_by_size),
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
                }],
            },
        });
    }
}
