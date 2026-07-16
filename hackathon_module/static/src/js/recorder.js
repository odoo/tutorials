import publicWidget from "@web/legacy/js/public/public_widget";

const CHUNK_INTERVAL_MS = 60000;
const VIDEO_BITS_PER_SECOND = 100_000;

publicWidget.registry.HackathonRecorder = publicWidget.Widget.extend({
    selector: ".o_hackathon_dashboard",
    events: {
        "click #startBtn": "_onStartRecording",
        "click #stopBtn": "_onStopRecording"
    },

    init() {
        this._super(...arguments);
        this.stream = null;
        this.timer = null;
        this.timeLeft = 28800;
        this.sessionId = null;
        this._uploadPromises = [];
    },

    start() {
        this.videoEl = this.el.querySelector("#webcamPreview");
        this.timerEl = this.el.querySelector("#timerDisplay");
        this.startBtn = this.el.querySelector("#startBtn");
        this.stopBtn = this.el.querySelector("#stopBtn");
        this._renderTimer();
        return this._super(...arguments);
    },

    destroy() {
        clearInterval(this.timer);
        this.stream?.getTracks().forEach((t) => t.stop());
        this._super(...arguments);
    },

    _renderTimer() {
        const pad = (n) => String(Math.floor(n)).padStart(2, "0");
        this.timerEl.textContent =
            `${pad(this.timeLeft / 3600)}:${pad((this.timeLeft % 3600) / 60)}:${pad(this.timeLeft % 60)}`;
    },
    _uploadChunk(blob) {
        const formData = new FormData();
        formData.append("chunk", blob, `${Date.now()}.webm`);
        formData.append("session_id", this.sessionId);

        const promise = fetch("/hackathon/upload_chunk", {
            method: "POST",
            body: formData,
        }).then((response) => {
            if (!response.ok) {
                console.warn("Chunk upload failed with status", response.status);
            }
        }).catch((err) => {
            console.warn("Chunk upload failed:", err);
        });

        this._uploadPromises.push(promise);
        return promise;
    },
    async _finalizeSession() {
        try {
            const formData = new FormData();
            formData.append("session_id", this.sessionId);

            const response = await fetch("/hackathon/finalize_session", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                this.displayNotification({
                    title: "Recording saved",
                    message: "Your session video has been saved successfully.",
                    type: "success",
                });
            } else {
                console.warn("Finalize failed with status", response.status);
                this.displayNotification({
                    title: "Save warning",
                    message: "Recording stopped but the final video could not be processed. Raw chunks are still on disk.",
                    type: "warning",
                });
            }
        } catch (err) {
            console.warn("Finalize request failed:", err);
        }
    },


    async _onStartRecording() {
        if (!("MediaRecorder" in window)) {
            this.displayNotification({
                title: "Not supported",
                message: "This browser cannot record video. Please use Chrome, Edge, or Firefox.",
                type: "danger",
            });
            return;
        }

        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 320 }, height: { ideal: 240 } },
                audio: false,
            });
            this.videoEl.srcObject = this.stream;

            const mime = ["video/webm;codecs=vp9", "video/webm"].find((t) =>
                MediaRecorder.isTypeSupported(t)
            ) || "video/webm";

            this.sessionId = `sess_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

            this.recorder = new MediaRecorder(this.stream, {
                mimeType: mime,
                videoBitsPerSecond: VIDEO_BITS_PER_SECOND,
            });

            this.recorder.ondataavailable = (e) => {
                if (e.data.size > 10000) {
                    this._uploadChunk(e.data);
                }
            };
            this.recorder.start(CHUNK_INTERVAL_MS);

            this.timer = setInterval(() => {
                if (this.timeLeft > 0) {
                    this.timeLeft--;
                    this._renderTimer();
                } else {
                    this._onStopRecording();
                }
            }, 1000);

            this.startBtn.disabled = true;
            this.stopBtn.disabled = false;
        } catch (err) {
            console.error(err);
            this.displayNotification({
                title: "Camera error",
                message: "Could not access the webcam. Please check your permissions.",
                type: "danger",
            });
        }
    },

    _onStopRecording() {
        if (this.recorder?.state !== "inactive") {
            this.recorder.onstop = async () => {
                await Promise.all(this._uploadPromises);
                this._finalizeSession();
            };
            this.recorder.stop();
        }
        this.stream?.getTracks().forEach((t) => t.stop());
        this.videoEl.srcObject = null;
        clearInterval(this.timer);
        this.timeLeft = 28800;
        this._renderTimer();
        this.startBtn.disabled = false;
        this.stopBtn.disabled = true;
    },
});
