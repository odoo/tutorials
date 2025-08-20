/** @odoo-module **/
import { Component, useRef, onWillStart, useEffect, onWillUnmount} from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
     static template = "awesome_dashboard.PieChart";
     static props = {
        data: {type: Object}
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");
         onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        })

        useEffect(() => {
            this.renderChart();
        });

        onWillUnmount(() => {

            if (this.chart) {
                this.chart.destroy();
            }
        })
       
    }


    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        const ctx = this.canvasRef.el.getContext("2d");
        const data = this.props.data || {};
        const labels = Object.keys(data);
        const values = Object.values(data);

        this.chart = new Chart(ctx, {
            type: "pie",
            data: {
                labels,
                datasets: [{
                    label: "T-Shirts Sold by Size",
                    data: values,
                    backgroundColor: [
                        "#FF6384", "#36A2EB", "#FFCE56"
                    ],
                }],
            },
            /*
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: "Shirt orders by size",
                        align: "start"
                    }
                }
            }*/
        });
        //Chart.animationService.advance();

    
    }
}
