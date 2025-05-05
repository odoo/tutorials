import { Component, onWillStart, useRef, onMounted, onWillUnmount, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";



export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        label: String,
        data: Object,
    };
    
    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(() => {
            this.renderChart();
        });
        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                this.updateChart(nextProps);
            }
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const colors = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: colors,
                    },
                ],
            },
        });
    }

    updateChart(nextProps) {
        const labels = Object.keys(nextProps.data);
        const data = Object.values(nextProps.data);
        const colors = labels.map((_, index) => getColor(index));

        this.chart.data.labels = labels;
        this.chart.data.datasets[0].label = nextProps.label;
        this.chart.data.datasets[0].data = data;
        this.chart.data.datasets[0].backgroundColor = colors;
        this.chart.update();
    }

}