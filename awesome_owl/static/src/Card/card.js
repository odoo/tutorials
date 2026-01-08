/** @odoo-module **/

import { Component, useState,xml } from "@odoo/owl";

export class Card extends Component {
    static template = 'awesome_owl.card';
    static props={
      'title':{type:String, optional:false},
      'content':{type:String}
    };
    
   
  }


