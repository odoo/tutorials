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
      uomType: null,
      secFactor: null,
      secUoms: [],
      secFactors: [],
      secUomType: null,
      factor: null,
      factors: [],
    });
    this.pos = usePos();
    this.categId = this.props.categId;
    this.uomId = this.props.uomId;
    this.productId = this.props.productId;

    onWillStart(async () => {
      //Find second UOM ID
      this.secondUomId = await this.orm.searchRead(
        "product.template",
        [["id", "=", this.productId]],
        ["sec_uom_id"]
      );
      if (!this.secondUomId[0].sec_uom_id) return;
      //Find second Category ID from product template
      this.categoryId = await this.orm.searchRead(
        "uom.uom",
        [["id", "=", this.secondUomId[0].sec_uom_id[0]]],
        ["category_id"]
      );
      //Find all the UOM id for the same category
      this.state.secUoms = await this.orm.searchRead(
        "uom.uom",
        [
          ["category_id", "=", this.categoryId[0].category_id[0]],
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
    //Find Second UOM Factor
    this.state.secFactors = await this.orm.searchRead(
      "uom.uom",
      [["id", "=", this.state.secUomId]],
      ["factor"]
    );
    //Find First UOM Factor
    this.state.factors = await this.orm.searchRead(
      "uom.uom",
      [["id", "=", this.uomId]],
      ["factor"]
    );
    //Find Second UOM Type
    this.state.secUomType = await this.orm.searchRead(
      "uom.uom",
      [["id", "=", this.state.secUomId]],
      ["uom_type"]
    );
    //Find First UOM Type
    this.state.uomType = await this.orm.searchRead(
      "uom.uom",
      [["id", "=", this.uomId]],
      ["uom_type"]
    );
    this.props.onConfirm(
      this.state.quantity,
      this.state.uomType[0].uom_type,
      this.state.secFactors[0].factor,
      this.state.factors[0].factor,
      this.state.secUomType[0].uom_type
    );
    this.props.close();
  }
  cancel(){
    this.props.close();
  }
}

patch(ControlButtons.prototype, {
  setup() {
    super.setup();
    this.pos = usePos();
    this.orm = this.env.services.orm;
    this.dialog = this.env.services.dialog;
    this.length = useState({ value: 0 });
    this.showCustomButton = useState({value: false})
    useEffect(
      () => {
        this.getProductIdsFromOrderlines();
      },
      () => [this.pos.get_order().get_selected_orderline()?.id]
    );
  },
  async getProductIdsFromOrderlines() {
    const order = this.pos.get_order();
    if (order.lines.length > 0) {
      const selectedOrder = order.get_selected_orderline().id;
      const currentOrder = order.lines.filter((id) => id.id == selectedOrder);
      this.categId = currentOrder[0].product_id.categ_id.id;
      this.uomId = currentOrder[0].product_id.uom_id.id;
      this.productId = currentOrder[0].product_id._raw.product_tmpl_id;
      const productData = await this.orm.searchRead(
        "product.template",
        [["id", "=", this.productId]],
        ["sec_uom_id"]
      );
      if (productData.length > 0 && productData[0].sec_uom_id) {
        this.showCustomButton.value = true;
      } else {
        this.showCustomButton.value = false;
      }
      if (!order) return [];
      return order.lines.map((line) => line.product_id.id);
      
    }
  },
  clickCustomButton() {
    this.dialog.add(ConfigurationDialog, {
      categId: this.categId,
      uomId: this.uomId,
      productId: this.productId,
      onConfirm: (quantity, uomType, secFactor, factor, secUomType) =>
        this.handleDialogConfirm(
          quantity,
          uomType,
          secFactor,
          factor,
          secUomType
        ),
    });
  },
  handleDialogConfirm(quantity, uomType, secFactor, factor, secUomType) {
    const orderline = this.currentOrder.get_selected_orderline();
    if (secUomType === "bigger") {
      orderline.set_quantity(quantity * secFactor);
    } else {
      if (uomType === "bigger") {
        orderline.set_quantity(quantity * factor);
      }
      if (uomType === "reference") orderline.set_quantity(quantity / secFactor);
    }
  },
});
