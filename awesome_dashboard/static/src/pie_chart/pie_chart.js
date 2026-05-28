import { Component, onMounted, onWillStart, onWillUnmount, useRef } from "@odoo/owl"
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";


export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart"
    static props = {
        data: Object,
        optional: true
    }

    setup() {
        this.state =
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js")
        })

        this.canvasRef = useRef("canvas");

        if (this.props.data) {
            onMounted(() => {
                const keys = Object.keys(this.props.data)
                const values = Object.values(this.props.data)
                const colors = keys.map((_, index) => getColor(index));

                this.chart = new Chart(this.canvasRef.el, {
                    type: "pie",
                    data: {
                        labels: keys,
                        datasets: [
                            {
                                backgroundColor: colors,
                                data: values,
                            },
                        ]
                    }
                });
            })

                    onWillUnmount(() => {
            this.chart.destroy();
        });
        }
    }
}
