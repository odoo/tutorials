import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = {
        data: { type: Object, element: Number },
        options: { type: Object, optional: true },
    };

    static defaultProps = {
        options: {},
    }

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        useEffect(() => {
            if (this.chart) {
                this.chart.destroy();
            }
            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    datasets: [{ data: Object.values(this.props.data) }],
                    labels: Object.keys(this.props.data),
                },
                options: this.props.options,
            });
        });
    }
}
