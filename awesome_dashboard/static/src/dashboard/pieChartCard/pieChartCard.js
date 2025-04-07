import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChartCard extends Component {
    static template = "awesome_dashboard.PieChartCard";

    static props = { 
        title:{
            type: String
        },
        value: {
            type: Object
        }
    };

    setup(){
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        useEffect(() => this.renderChart());
    }
    

    renderChart() {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvasRef.el,{
            type: 'pie',
            data: {
                labels: Object.keys(this.props.value),
                datasets: [{
                    data: Object.values(this.props.value),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {}
        });
    }
}
