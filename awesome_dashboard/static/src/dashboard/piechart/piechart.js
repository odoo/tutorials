import { Component, useState, useRef, onMounted, onWillStart, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";;

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.canvasRef = useRef("canvas");
        this.statistics = useState(this.statisticsService.data);

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
                labels: Object.keys(this.statistics.orders_by_size),
                datasets: [{
                    label: "T-Shirts Sold",
                    data: Object.values(this.statistics.orders_by_size),
                    backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
                }]
            }
        });
    }

    updateChart() { 
        if (!this.chart || !this.statistics.orders_by_size) return;

        this.chart.data.labels = Object.keys(this.statistics.orders_by_size);
        this.chart.data.datasets[0].data = Object.values(this.statistics.orders_by_size);
        this.chart.update();
    }
}
