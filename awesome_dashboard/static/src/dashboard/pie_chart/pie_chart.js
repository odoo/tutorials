import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => this.renderChart());
        onWillUnmount(() => this.chart?.destroy());
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));

        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels,
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

    onPieClick(e) {
        var slice = this.chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true);
        if (!slice.length) return;
        var label = this.chart.data.labels[slice[0].index];
        alert("Redirect to orders of size: " + label);
    }
}
