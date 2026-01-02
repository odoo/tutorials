import { Component, onWillStart, onMounted, xml, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = xml`
        <canvas t-ref='chart'/>
    `
    setup(){
        this.chartRef = useRef('chart');

        onWillStart( async () => {
            await loadJS('/web/static/lib/Chart/Chart.js');
        });
        onMounted(()=>{
            this.pieChart = new Chart(this.chartRef.el, {
                type: 'pie',
                data: {
                    datasets: [
                        { 
                            data: Object.values(this.props.data)
                        }
                    ],
                    labels: Object.keys(this.props.data),
                },
            });
        })
    }
}