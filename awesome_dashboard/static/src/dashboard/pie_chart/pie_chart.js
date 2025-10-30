import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title: {type: String},
        data: {type: Object},
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
         onMounted(() => {
            this.renderChart();
        });
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
                        label: this.props.title,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
        });
    }
}
