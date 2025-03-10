import BarcodePickingModel from "@stock_barcode/models/barcode_picking_model";


export class SetDefaultLocation extends BarcodePickingModel {
  _getNewLineDefaultContext() {
    return {
      default_location_id: this.lastScanned.sourceLocation
        ? this.lastScanned.sourceLocation.id
        : this._defaultLocation().id,
    };
  }
}
