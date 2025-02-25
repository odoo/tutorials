/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, onWillStart, useState, useEffect } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

class ConfigurationDialog extends Component {
  static template = "pos_second_uom.ConfigurationDialog";
  static components = { Dialog };

  setup() {
    this.orm = this.env.services.orm;
    this.state = useState({
      quantity: 1,
      secUomId: null,
      factor: null,
      secUoms: [],
      factors: [],
      uomType: null
    });
    this.pos = usePos();
    this.categId = this.props.categId;
    this.uomId = this.props.uomId;
    this.productId = this.props.productId

    onWillStart(async () => {
      this.secondUomId = await this.orm.searchRead(
        "product.template",
        [
          ["id", "=", this.productId],
        ],
        ["id", "sec_uom_id"]
      );
      console.log(this.secondUomId[0].sec_uom_id[0])
      this.state.secUoms = await this.orm.searchRead(
        "uom.uom",
        [
          ["category_id", "=", this.categId],
          ["id", "!=", this.uomId],
        ],
        ["id", "name"]
      );
      if (this.state.secUoms.length > 0) {
        this.state.secUomId = this.state.secUoms[0].id;
      }
    });
  }

  updateQuantity(event) {
    this.state.quantity = event.target.value;
  }

  updateUom(event) {
    this.state.secUomId = parseInt(event.target.value);
  }

  async done() {
    this.state.factors = await this.orm.searchRead(
      "uom.uom",
      [["id", "=", this.state.secUomId]],
      ["id", "factor"]
    );
    this.state.uomType = await this.orm.searchRead(
      "uom.uom",
      [["id", "=", this.state.secUomId]],
      ["id", "uom_type"]
    );
    console.log(this.state.secUomId)
    this.props.onConfirm(
      this.state.quantity,
      this.state.secUomId,
      this.state.factors[0].factor,
      this.state.uomType[0].uom_type
    );
    this.props.close();
  }
}

patch(ControlButtons.prototype, {
  setup() {
    super.setup();
    this.pos = usePos();
    this.orm = this.env.services.orm;
    this.dialog = this.env.services.dialog;
    this.r = useState({ value: [] });
    useEffect(
      () => {
        this.loadSecUomId();
      },
      () => [this.pos.get_order().get_selected_orderline().id]
    );
  },
  getProductIdsFromOrderlines() {
    const order = this.pos.get_order();
    const selectedOrder = order.get_selected_orderline().id;
    const currentOrder = order.lines.filter((id) => id.id == selectedOrder);
    this.categId = currentOrder[0].product_id.categ_id.id;
    this.uomId = currentOrder[0].product_id.uom_id.id;
    this.productId = currentOrder[0].product_id._raw.product_tmpl_id;
    console.log(currentOrder[0])
    if (!order) return [];
    return order.lines.map((line) => line.product_id.id);
  },
  async loadSecUomId() {
    const productIds = this.getProductIdsFromOrderlines();
    if (productIds.length === 0) {
      this.r.values = []; // No products in orderline
      return;
    }
    this.r.values = await this.orm.searchRead(
      "product.template",
      [["id", "in", productIds]],
      ["uom_id", "sec_uom_id"]
    );
  },
  clickCustomButton() {
    this.dialog.add(ConfigurationDialog, {
      categId: this.categId,
      uomId: this.uomId,
      productId: this.productId,
      onConfirm: (quantity, secUomId, factor, uomType) =>
        this.handleDialogConfirm(quantity, secUomId, factor, uomType),
    });
  },
  handleDialogConfirm(quantity, secUomId, factor, uomType) {
    const orderline = this.currentOrder.get_selected_orderline();
    console.log(factor)
    if(uomType === "smaller")
      orderline.set_quantity(quantity / factor);
    else
      orderline.set_quantity(quantity * factor);
  },
});
