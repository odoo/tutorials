import { patch } from '@web/core/utils/patch';
import { PosOrder } from '@point_of_sale/app/models/pos_order';

patch(PosOrder.prototype, {
    removeOrderline(line) {
        debugger
        let subProductIds = new Set(line.product_id.sub_product_ids.map((sub) => sub.id));
        let linesToRemove = this.lines.filter((x) => subProductIds.has(x.product_id.id));
        linesToRemove.forEach((line) => super.removeOrderline(line));
        return super.removeOrderline(line)
    }
})
