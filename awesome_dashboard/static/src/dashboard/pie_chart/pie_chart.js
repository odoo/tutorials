import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount, onPatched } from "@odoo/owl";
export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };
    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });
        onPatched(() => {
            this.updateChart();
        });


        // onWillUnmount(() => {
        //     this.chart.destroy();
        // });
    }
    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
        });
    }

    updateChart() {
        if (this.chart) {
            // Update chart data
            this.chart.data.labels = Object.keys(this.props.data);
            this.chart.data.datasets[0].data = Object.values(this.props.data);
            this.chart.update();
        } else {
            this.renderChart();
        }
    }
}