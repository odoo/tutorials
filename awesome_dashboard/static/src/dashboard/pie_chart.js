import { Component, onMounted, onPatched, onWillStart, onWillUnmount, useRef } from "@odoo/owl";

import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";

    static props = {
        data: {
            type: Object,
        },
        label: {
            type: String
        }
    }

    setup() {
        this.chartRef = useRef("pie_chart");

        onWillStart(() => loadJS("https://cdn.jsdelivr.net/npm/chart.js"));

        onMounted(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            this.chart.destroy();
        });

        onPatched(() => {
            this.chart.destroy();
            this.renderChart();
        });
    }

    renderChart() {
        const a = Object.keys(this.props.data);
        const b = Object.values(this.props.data)
        this.chart = new Chart(this.chartRef.el, {
            type: 'pie',
            data: {
                labels: a,
                datasets: [{
                    label: this.props.label,
                    data: b,
                    borderWidth: 1
                }]
            }
        });
    }
}
