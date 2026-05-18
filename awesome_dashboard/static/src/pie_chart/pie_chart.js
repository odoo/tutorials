import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onMounted, onWillStart, onWillUnmount, useRef } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        data: Object,
        label: String,
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => this.renderChart());
        onWillUnmount(() => this.chart.destroy());
    }

    renderChart() {
        const configs = this.getConfigs();
        const options = this.getOptions();
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: configs,
            options: options,
        });
    }

    getConfigs() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));
        const configs = {
            labels: labels,
            datasets: [
                {
                    data: data,
                    backgroundColor: color,
                },
            ],
        };
        return configs;
    }

    getOptions() {
        const options = {
            plugins: {
                title: {
                    display: true,
                    text: this.props.label,
                    align: "start",
                },
            },
        };
        return options;
    }
}
