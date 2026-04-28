import { Component, onMounted, onPatched, onWillStart, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: {
            type: Object,
        }
    }

    setup() {
        this.canvas = useRef("canvas");
        onWillStart(async () => await loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onPatched(() => {
            this.renderChart();
            this.destroyChart();
        });
        onWillUnmount(() => this.destroyChart());
    }

    destroyChart() {
        if (this.chart) {
            this.chart.destroy();
        }
    }

    renderChart() {
        this.chart = new Chart(this.canvas.el, {
            type: "pie", data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        data: Object.values(this.props.data),
                    },
                ],
            }
        });
    }
}
