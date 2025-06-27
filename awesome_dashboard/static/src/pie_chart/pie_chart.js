import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, onWillUnmount, onMounted, onWillUpdateProps, useRef } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: { type: String, optional: true },
        data: { type: Object, optional: true },
    };

    setup(){
        this.canvasRef = useRef("canvas");
        onWillStart (() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        });
        onWillUpdateProps((nextProps) => {
            this.chart.destroy();
            this.renderChart(nextProps);
        })
        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    };

    renderChart(props = this.props) {
        const labels = Object.keys(props.data);
        const data = Object.values(props.data);
        const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
        });
    }
}
