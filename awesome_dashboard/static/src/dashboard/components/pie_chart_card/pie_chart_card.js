import { Component, onWillStart, onMounted, useRef, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";


export class PieChartCard extends Component {
    static template = "awesome_dashboard.pie_chart"

    setup() {
        this.canvasRef = useRef("canvas")

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js")
        })
        onMounted(() => {
            this.renderChart();
        });
        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.chart.destroy();
            }
            this.renderChart(nextProps.data);
        });
    }

    renderChart() {
        this.chart = new Chart(this.canvasRef.el.getContext("2d"), {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: this.props.title,
                    data: Object.values(this.props.data),
                    backgroundColor: ["#007BFF", "#FFA500", "#808090"]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            },
        })
    }
}
