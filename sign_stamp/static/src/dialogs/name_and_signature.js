import { renderToString } from "@web/core/utils/render";
import { patch } from "@web/core/utils/patch";
import { NameAndSignature } from "@web/core/signature/name_and_signature";

patch(NameAndSignature.prototype, {

    async drawCurrentName() {
        if(this.props.signatureType === 'stamp'){
            const font = this.fonts[this.currentFont];
            const stampData = this.getStampData();
            const canvas = this.signatureRef.el;
            const img = this.getSVGStamp(font, stampData, canvas.width, canvas.height);
            await this.printImage(img);
        }
        else{
            super.drawCurrentName()
        }
    },

    getStampData() {
        return {
            name: this.props.signature.name,
            company: this.props.signature.company,
            address: this.props.signature.address,
            city: this.props.signature.city,
            country: this.props.signature.country,
            vat: this.props.signature.vat,
            logo: this.props.signature.logo
        };
    },

    getSVGStamp(font, stampData, width, height) {
        const svg = renderToString("sign_stamp.sign_svg_stamp", {
            width: width,
            height: height,
            font: font,
            name: stampData.name,
            company: stampData.company,
            address: stampData.address,
            city: stampData.city,
            country: stampData.country,
            vat: stampData.vat,
            color: this.props.fontColor,
            logo: stampData.logo
        });

        return "data:image/svg+xml," + encodeURI(svg);
    },

    onInputData(ev) {
        if(ev.target.name === 'logo'){
            const file = ev.target.files[0]; // Get the selected file
            if (file) {
                const reader = new FileReader();
                reader.onload = () => {
                    this.props.signature.logo = reader.result
                    this.drawCurrentName();
                };
                reader.readAsDataURL(file);
            }
        }
        else{
            this.props.signature[ev.target.name] = ev.target.value;
        }
        if (!this.state.showSignatureArea && this.getStampData()) {
            this.state.showSignatureArea = true;
            return;
        }
        if (this.state.signMode === "auto") {
            this.drawCurrentName();
        }
    },

    getSVGTextFont(font) {
        const height = 100;
        const width = parseInt(height * this.props.displaySignatureRatio);
        if(this.props.signatureType === 'stamp'){
            return this.getSVGStamp(font, this.getStampData(), width, height);
        }
        else{
            return super.getSVGTextFont(font)
        }
    }
})
