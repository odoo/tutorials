import { Component, onWillStart, onMounted, useRef, useState,onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
  static template = "awesome_dashboard.pie";
  static props={
    data:{
      type:Object,
      optional:false
    }
  }
  setup() {
    this.action=useService("action")
    this.canvasRef = useRef("canvas");
    this.statistics = useService("awesome_dashboard.statistics");
    this.state = useState({
      res: this.statistics.data,
    });
    onWillStart(async () => {       
      await loadJS("/web/static/lib/Chart/Chart.js");
    });

    onMounted(() => {
        this.renderChart();
      
    });
    onWillUpdateProps((nextProp)=>{
      if(this.chart){
        this.chart.destroy()
      }
      this.renderChart()
    })
  }
  openOrdersBySize(index) {
    // this.action.doAction("sale.order");
      this.action.doAction("base.action_partner_form");

  }
  
  renderChart() {
    const data=this.props.orders_by_size  
    
    if (!this.canvasRef.el) {
      console.error("Canvas element is not available.");
      return;
    }

    if (this.chart) {
      this.chart.destroy();
    }

    const ctx = this.canvasRef.el.getContext("2d");
    this.chart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["S", "M", "XL"],
        datasets: [
          {
            data: [
              data?.s || 0,
              data?.m || 0,
              // data?.l || 0,
              data?.xl || 0,
              data?.xxl || 0,
            ],
            backgroundColor: ["#FF6384", "#36A2EB", "#4BC0C0"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index;
            
            const size = ["S", "M", "XL"][index];  // FIXED: Get size from index
            console.log(index," ",size);
            this.openOrdersBySize(index);  // FIXED: Pass only size, not { size: label }
          }
      },
      },
    });
  }
}
