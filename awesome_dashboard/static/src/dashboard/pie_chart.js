import { Component, onMounted, onWillStart, useEffect, useRef, useState } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.canvasRef = useRef("canvas");
        this.statistics = useState(this.statisticsService.statistics);

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        useEffect(() => {
            this.updateChart();
        }, () => Object.values(this.statistics));
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.statistics.sizedata || []),
                datasets: [{
                    label: "T-Shirts Sold",
                    data: Object.values(this.statistics.sizedata || []),
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"],
                }]
            }
        });
    }

    updateChart() {
        this.chart.data.labels = Object.keys(this.statistics.sizedata);
        this.chart.data.datasets[0].data = Object.values(this.statistics.sizedata);
        this.chart.update();
    }
}
