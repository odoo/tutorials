import { patch } from "@web/core/utils/patch";
import { Document } from "@sign/components/sign_request/document_signable";

patch(Document.prototype, {
  getDataFromHTML() {
    super.getDataFromHTML();
    const { el: parentEl } = this.props.parent;

    const fields = ["company", "address", "city", "country", "vat", "logo"];

    this.signerInfo = {};

    for (const field of fields) {
      const element = parentEl.querySelector(
        `#o_sign_signer_${field}_input_info`
      );
      this.signerInfo[field] = element?.value;
    }
  },

  get iframeProps() {
    return {
      ...super.iframeProps,
      ...this.signerInfo,
    };
  },
});
