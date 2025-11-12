import { Component, onWillStart, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.piechart";
    static props = {
        label: String,
        data: Object,
    }

    setup() {
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.canvasRef = useRef("pieChartCanvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.renderChart();
        });
    }

    renderChart() {
        if (!this.props.data || typeof this.props.data !== "object") {
            console.error("Invalid data:", this.props.data);
            return;
        }

        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: [
                            "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF" 
                        ],
                    }
                ]
            },
        });
    }
}
