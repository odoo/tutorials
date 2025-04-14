import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { fuzzyLookup } from "@web/core/utils/search";
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Input } from "@point_of_sale/app/generic_components/inputs/input/input";
import { Component, useState } from "@odoo/owl";
import { unaccent } from "@web/core/utils/strings";
import { SalesPersonLine } from "../SalesPersonLine/SalesPersonLine";

export class SalesPersonList extends Component {
  static template = "pos_salesperson.SalesList";
  static components = { SalesPersonLine, Dialog, Input };
  static props = {
    salesperson: {
      optional: true,
      type: [{ value: null }, Object],
    },
    getPayload: { type: Function },
    close: { type: Function },
  };
  setup() {
    this.pos = usePos();
    this.ui = useState(useService("ui"));
    // this.dialog = useService("dialog");
    this.state = useState({
      query: null,
    });
  }

  getSalesPerson() {
    const searchWord = unaccent((this.state.query || "").trim(), false);
    const salesperson = this.pos.models["hr.employee"].getAll();
    const exactMatches = salesperson.filter(
      (person) => (person.name || "").toLowerCase() === searchWord.toLowerCase()
    );

    if (exactMatches.length > 0) {
      return exactMatches;
    }
    const availableSalesPerson = searchWord
      ? fuzzyLookup(searchWord, salesperson, (sale) =>
          unaccent(sale.searchString || "", false)
        )
      : salesperson.slice(0, 100).toSorted((a, b) => {
          if (this.props.salesperson && this.props.salesperson.id === a.id) {
            return -1;
          }
          return (a.name || "").localeCompare(b.name || "");
        });

    return availableSalesPerson;
  }

  clickSalesPerson(salesperson) {
    this.props.getPayload(salesperson);
    this.props.close();
  }
}
