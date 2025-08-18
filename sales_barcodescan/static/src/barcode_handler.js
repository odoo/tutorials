import { patch } from "@web/core/utils/patch";
import { ProductCatalogKanbanController } from "@product/product_catalog/kanban_controller";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { onMounted, onWillUnmount } from "@odoo/owl";

patch(ProductCatalogKanbanController.prototype, {
  setup(){
    super.setup();
    this.orm = useService("orm");
    this.notification = useService("notification");
    this.orderId = this.props.context.order_id;
    this.orderResModel = this.props.context.product_catalog_order_model;
    this.lastInputTime = 0;
    this.barcodeBuffer = "";
    this._onKeyDown = this._onKeyDown.bind(this);
    onMounted(() => {
      document.addEventListener("keydown", this._onKeyDown);
    });
    onWillUnmount(() => {
      document.removeEventListener("keydown", this._onKeyDown);
    });
  },

  async _onKeyDown(res) {
    const targetfield = res.target.tagName;
    if (targetfield === "INPUT" || targetfield === "TEXTAREA" || targetfield === "SELECT") {
      return;
    }
    const currentTime = new Date().getTime();
    if (currentTime - this.lastInputTime > 800) {
      this.barcodeBuffer = "";
    }
    if (res.key === "Enter") {
      if (this.barcodeBuffer.length > 1) {
        this._processBarcode(this.barcodeBuffer);
        this.barcodeBuffer = "";
      }
    } else if (res.key.length === 1) {
      this.barcodeBuffer += res.key;
    }
    this.lastInputTime = currentTime;
  },

  async _processBarcode(scannedBarcode) {
    if (!this.orderId) {
      this.notification.add("Please select an order first.", {
        type: "warning",
      });
      return;
    }
    try {
      const products = await this.orm.searchRead(
        "product.product",
        [["barcode", "=", scannedBarcode]],
        ["id", "name"]
      );

      if (!products.length) {
        this.notification.add("No product found for this barcode.", {
          type: "warning",
        });
        return;
      }

      const product = products[0];

      let orderLineModel, quantityField;
      if (this.orderResModel === "sale.order") {
        orderLineModel = "sale.order.line";
        quantityField = "product_uom_qty";
      } else if (this.orderResModel === "purchase.order") {
        orderLineModel = "purchase.order.line";
        quantityField = "product_qty";
      } else {
        console.error(
          "Unsupported order model for barcode scanning:",
          this.orderResModel
        );
        this.notification.add(
          "Barcode scanning is not supported for this type of model.",
          { type: "danger" }
        );
        return;
      }

      const existingOrderLines = await this.orm.searchRead(
        orderLineModel,
        [
          ["order_id", "=", this.orderId],
          ["product_id", "=", product.id],
        ],
        ["id", quantityField]
      );

      const updatedQuantity = existingOrderLines.length ? existingOrderLines[0][quantityField] + 1 : 1;

      const response = await rpc("/product/catalog/update_order_line_info", {
        res_model: this.orderResModel,
        order_id: this.orderId,
        product_id: product.id,
        quantity: updatedQuantity,
      });

      if (response && response.success) {
        this.notification.add(
          `successfully ${existingOrderLines ? "Updated" : "Added"} ${product.name} (Qty: ${updatedQuantity})`,
          { type: "success" }
        );
        this.model.load();
      } else {
        this.notification.add(
          `failed to ${existingOrderLines ? "update" : "add"} ${product.name}.`,
          { type: "danger" }
        );
        this.model.load();
      }
      this.model.load();
    } catch (error) {
      console.error("Error processing barcode scan:", error);
      this.notification.add("An error occurred while processing the barcode.", {
        type: "danger",
      });
    }
  },
});
