import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_owl.pie_chart";
    static props = {
        data: {
            type: Object,
        },
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");

        });

        useEffect(() => {
            this.chart = new Chart(this.canvasRef.el, {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [
                        {
                            data: Object.values(this.props.data),
                        },
                    ],
                },
            });
            return () => {
                this.chart.destroy();
            }
        });
    }



}
