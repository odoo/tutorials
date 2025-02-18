import { Component, useState} from "@odoo/owl";

export class Card extends Component{
      
       static template = "awesome_owl.Card"
       static props = {
              
              title : {
                  type : String,
                  required : true
              },
              content : {
                  type : String,
                  required : true
              }
       }
}