import { Component, useRef, onMounted, onWillStart, onWillUnmount } from "@odoo/owl";
import { getColor } from "@web/core/colors/colors";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_owl.PieChart";
    static props = {
        label: String,
        data: Object,
    };
    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;
        onWillStart(() => {
            loadJS("/web/static/lib/Chart/Chart.js");
        });
        onMounted(() => {
            this.renderChart();
        });
        // onWillUnmount(() => {
        //     this.chart.destroy();
        // })
    };

    renderChart() {
        if (this.props.data) {
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
        } else {
            console.log("Can't load data!!")
        }
    }
}
