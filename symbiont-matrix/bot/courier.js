// Thin Minecraft transport adapter.
// Policy, trust, authority and message interpretation stay outside this file.
const mineflayer = require("mineflayer");
const WebSocket = require("ws");
const { randomUUID } = require("crypto");

const NODE_ID = process.env.NODE_ID || "courier-01";
const MC_HOST = process.env.MC_HOST || "127.0.0.1";
const MC_PORT = Number(process.env.MC_PORT || 25565);
const MC_VERSION = process.env.MC_VERSION || undefined;
const RUNTIME_WS = process.env.RUNTIME_WS || "ws://127.0.0.1:9999";
const SAMPLE_MS = Number(process.env.SAMPLE_MS || 1000);

let ws, bot, sequence = 0, observationTimer;

function emit(eventType, payload, epistemic = "CLAIMED") {
  if (!ws || ws.readyState !== WebSocket.OPEN) return;
  sequence += 1;
  ws.send(JSON.stringify({
    event_id: randomUUID(), node_id: NODE_ID,
    session_id: bot?.player?.uuid || "unknown",
    event_type: eventType, observed_at: Date.now(), clock: sequence,
    payload, epistemic
  }));
}

function connectRuntime() {
  ws = new WebSocket(RUNTIME_WS);
  ws.on("open", () => emit("NODE_CONNECTED", { version: MC_VERSION || "auto" }, "OBSERVED"));
  ws.on("close", () => setTimeout(connectRuntime, 3000));
  ws.on("error", e => console.error("[courier] runtime:", e.message));
  ws.on("message", raw => {
    let command;
    try { command = JSON.parse(raw.toString()); } catch { return; }
    if (command.type === "DISCONNECT") bot?.quit();
  });
}

function connectMinecraft() {
  bot = mineflayer.createBot({
    host: MC_HOST, port: MC_PORT, username: NODE_ID,
    ...(MC_VERSION ? { version: MC_VERSION } : {})
  });

  bot.once("spawn", () => {
    emit("BOT_SPAWNED", {
      position: { x: bot.entity.position.x, y: bot.entity.position.y, z: bot.entity.position.z },
      dimension: bot.game.dimension
    }, "OBSERVED");

    observationTimer = setInterval(() => {
      if (!bot?.entity) return;
      const p = bot.entity.position;
      emit("OBSERVATION_POSITION", {
        x: p.x, y: p.y, z: p.z,
        yaw: bot.entity.yaw, pitch: bot.entity.pitch,
        bounds_status: "UNKNOWN"
      }, "OBSERVED");
    }, SAMPLE_MS);
  });

  bot.on("chat", (username, message) => {
    if (username !== bot.username) emit("CHAT_RECEIVED", { from: username, message }, "OBSERVED");
  });

  bot.on("end", () => {
    if (observationTimer) clearInterval(observationTimer);
    emit("BOT_DISCONNECTED", {}, "OBSERVED");
    setTimeout(connectMinecraft, 5000);
  });

  bot.on("error", e => console.error("[courier] minecraft:", e.message));
}

connectRuntime();
connectMinecraft();
