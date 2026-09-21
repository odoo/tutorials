import { Component, onWillStart, useRef, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        onWillUnmount(() => {
            this.cleanChart();
        });

        onWillUpdateProps((nextProps) => {
            // TODO : Check when it is usefull to update the chart.
            this.cleanChart();
            this.renderChart();
        });

    }

    renderChart() {
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: Object.keys(this.props.data),
                datasets: [{
                    label: this.props.label,
                    data: Object.values(this.props.data),
                }],
            },
        });
    }

    cleanChart() {
        this.chart.destroy();
    }
}
