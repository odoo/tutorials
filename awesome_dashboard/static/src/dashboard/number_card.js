import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static template = xml`<div>
	  <p class="font-weight-bold"><t t-out="props.title"/></p>
	  <p class="text-success fs-2 text-center"><t t-out="props.value"/></p>
  </div>`;
}
