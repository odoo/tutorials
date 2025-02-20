import { Component,useState } from "@odoo/owl";


export class Card extends Component {
  static template = "awesome_owl.card";

  setup(){
    this.cardOpen = useState({value:true})
  }

  static props = {
    title: String,
    html: String,
    slots: {type:Object,optional:true}
  };
}
