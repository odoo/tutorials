import { Component, onWillStart, onPatched, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        items: {
            type: Object,
            optional: true,
            default: () => ({}),
        },
    }

    setup() {
        this.chartRef = useRef("pie-canvas");
        this.myPieChart = null;
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart()
        });
        onPatched(() => {
            this.renderChart()
        });
    }

    renderChart() {
        if (!this.chartRef.el) {
            return;
        }
        if (this.myPieChart) {
            this.myPieChart.destroy();
        }
        this.pieChartData = {
            labels: ['M', 'S', 'XL'],
            datasets: [{
                label: 'Sales Count',
                data: [this.props.items.m, this.props.items.s, this.props.items.xl],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        };
        this.pieChartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        };
        this.myPieChart = new Chart(this.chartRef.el, {
            type: 'pie',
            data: this.pieChartData,
            options: this.pieChartOptions
        });
    }
}
