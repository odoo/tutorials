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
    this.pos = usePos();

    // Initialize state variables
    this.state = useState({
      quantity: 1,
      secUomId: null,
      uomType: null,
      secFactor: null,
      secUoms: [],
      secUomType: null,
      factor: null,
    });

    this.productId = this.props.productId;
    this.uomId = this.props.uomId;

    // Fetch secondary UOMs before rendering
    onWillStart(async () => {
      const productData = await this.orm.searchRead(
        "product.template",
        [["id", "=", this.productId]],
        ["sec_uom_id"]
      );

      if (!productData.length || !productData[0].sec_uom_id) return;

      const secUomId = productData[0].sec_uom_id[0];

      // Retrieve the category ID of the secondary UOM
      const categoryData = await this.orm.searchRead(
        "uom.uom",
        [["id", "=", secUomId]],
        ["category_id"]
      );
      if (!categoryData.length) return;

      const categoryId = categoryData[0].category_id[0];

      // Fetch all UOMs in the same category
      const secUomsData = await this.orm.searchRead(
        "uom.uom",
        [["category_id", "=", categoryId]],
        ["id", "name"]
      );

      this.state.secUoms = secUomsData;
      this.state.secUomId = secUomsData.length ? secUomsData[0].id : null;
    });
  }

  // Update quantity when input changes
  updateQuantity(event) {
    this.state.quantity = Number(event.target.value);
  }

  // Update selected secondary UOM
  updateUom(event) {
    this.state.secUomId = parseInt(event.target.value);
  }

  // Confirm selection and pass values back to parent component
  async done() {
    const [secUomData, firstUomData] = await Promise.all([
      this.orm.searchRead(
        "uom.uom",
        [["id", "=", this.state.secUomId]],
        ["factor", "uom_type"]
      ),
      this.orm.searchRead(
        "uom.uom",
        [["id", "=", this.uomId]],
        ["factor", "uom_type"]
      ),
    ]);

    this.props.onConfirm(
      this.state.quantity,
      firstUomData[0]?.uom_type,
      secUomData[0]?.factor,
      firstUomData[0]?.factor,
      secUomData[0]?.uom_type
    );
    this.props.close();
  }

  // Close dialog without saving
  cancel() {
    this.props.close();
  }
}

// Patch ControlButtons to integrate the ConfigurationDialog
patch(ControlButtons.prototype, {
  setup() {
    super.setup();
    this.pos = usePos();
    this.orm = this.env.services.orm;
    this.dialog = this.env.services.dialog;
    this.showCustomButton = useState({ value: false });

    // Monitor selected order line and update state
    useEffect(
      () => {
        this.getProductIdsFromOrderlines();
      },
      () => [this.pos.get_order().get_selected_orderline()?.id]
    );
  },

  // Retrieve product details from the selected order line
  async getProductIdsFromOrderlines() {
    const order = this.pos.get_order();
    if (!order || order.lines.length === 0) return;

    const selectedOrder = order.get_selected_orderline();
    if (!selectedOrder) return;

    this.productId = selectedOrder.product_id._raw.product_tmpl_id;
    this.uomId = selectedOrder.product_id.uom_id.id;

    // Check if the product has a secondary UOM
    const productData = await this.orm.searchRead(
      "product.template",
      [["id", "=", this.productId]],
      ["sec_uom_id"]
    );

    this.showCustomButton.value =
      productData.length > 0 && productData[0].sec_uom_id;
  },

  // Open the ConfigurationDialog
  clickCustomButton() {
    this.dialog.add(ConfigurationDialog, {
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

  // Apply selected UOM conversion to order line quantity
  handleDialogConfirm(quantity, uomType, secFactor, factor, secUomType) {
    const orderline = this.pos.get_order().get_selected_orderline();
    if (!orderline) return;

    if (secUomType === "bigger") {
      orderline.set_quantity(quantity * secFactor);
    } else {
      orderline.set_quantity(
        uomType === "bigger" ? quantity * factor : quantity / secFactor
      );
    }
  },
});
