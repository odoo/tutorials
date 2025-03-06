// /** @odoo-module **/

// import { Component, useState, onMounted } from "@odoo/owl";
// import { registry } from "@web/core/registry";
// import { useService } from "@web/core/utils/hooks";

// export class AuctionStageSelector extends Component {
//     setup() {
//         this.rpc = useService("rpc");
//         this.state = useState({
//             auctionStage: this.props.initialStage || "template",
//             showDropdown: false,
//         });

//         onMounted(() => {
//             this.updateButtonStyle();
//         });
//     }

//     setAuctionStage(stage) {
//         this.state.auctionStage = stage;
//         this.state.showDropdown = false;
//         this.updateButtonStyle();

//         // Send updated value to Odoo
//         this.rpc({
//             model: "estate.property",
//             method: "write",
//             args: [[this.props.recordId], { auction_stage: stage }],
//         });
//     }

//     updateButtonStyle() {
//         const button = this.el.querySelector("#auction_stage_button");
//         if (!button) return;

//         button.classList.remove("btn-primary", "btn-warning", "btn-success");

//         if (this.state.auctionStage === "template") {
//             button.classList.add("btn-primary");
//         } else if (this.state.auctionStage === "in_progress") {
//             button.classList.add("btn-warning");
//         } else if (this.state.auctionStage === "sold") {
//             button.classList.add("btn-success");
//         }
//     }

//     get buttonText() {
//         return {
//             template: "Template",
//             in_progress: "In Progress",
//             sold: "Sold",
//         }[this.state.auctionStage] || "Template";
//     }
// }

// AuctionStageSelector.template = "estate.AuctionStageSelector";

// // ✅ Properly register the component
// registry.category("components").add("AuctionStageSelector", AuctionStageSelector);
