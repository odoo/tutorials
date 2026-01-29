import { loadJS } from "@web/core/assets";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, useEffect } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => this.renderChart());
        onWillUnmount(() => this.chart.destroy());
    }

    renderChart() {

        if (this.chart) {
            this.chart.destroy();
        }

        if (!this.props.data) {
            return;
        }

        const config = {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [
                    {
                        label: this.props.title,
                        data: Object.values(this.props.data),
                    },
                ],
            },
        };

        this.chart = new Chart(this.canvasRef.el, config);

    }

}
