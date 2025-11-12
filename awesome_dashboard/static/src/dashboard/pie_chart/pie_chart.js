import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
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
        onWillUnmount(() => {
            this.pie_chart.destroy();
        });
    }

    renderChart() {
        const size = Object.keys(this.props.data);
        const quantity = Object.values(this.props.data);
        const color = size.map((_, index) => getColor(index * 4));
        this.pie_chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: size,
                datasets: [
                    {
                        label: this.props.label,
                        data: quantity,
                        backgroundColor: color,
                    },
                ],
            },
        });
    }
}