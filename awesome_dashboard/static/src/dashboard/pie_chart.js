import { Component, onWillStart,useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        label: String,
        data : Object,
    }
    setup(){
        this.canvasRef = useRef("canvas_pie");
        onWillStart(async () => loadJS("/web/static/lib/Chart/Chart.js"));
        onMounted(()=> {
            this.renderChart();
            }   
        );
        onWillUnmount(()=> {
            this.chart.destroy();
        });


    }

    renderChart(){
        this.chart = new Chart(this.canvasRef.el,{
            type: 'pie',
            data : {
                labels : Object.keys(this.props.data),
                datasets:[
                    {
                    label: this.props.label,
                    data : Object.values(this.props.data),
                    },
                ],
            }
        })

    }
}

