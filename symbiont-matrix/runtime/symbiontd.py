"""Minimal event-to-evidence runtime."""
import asyncio, json, os, signal, time, uuid
import websockets
from .ledger import EvidenceLedger
from .rules import RuleEngine
from .schemas import Event, Evidence, hash_payload

RUNTIME_NODE_ID = os.environ.get("RUNTIME_NODE_ID", "symbiontd-01")
WS_HOST = os.environ.get("WS_HOST", "127.0.0.1")
WS_PORT = int(os.environ.get("WS_PORT", "9999"))
LEDGER_PATH = os.environ.get("LEDGER_PATH", "./data/evidence.jsonl")
RULES_DIR = os.environ.get("RULES_DIR", "./rules")

class Runtime:
    def __init__(self):
        self.ledger = EvidenceLedger(LEDGER_PATH)
        self.rules = RuleEngine(RULES_DIR)
        self.clock = self.ledger.last_clock
        self._shutdown = False

    def write_evidence(self, event, verdicts):
        self.clock = max(self.clock, event.clock) + 1
        payload = {
            "event": event.__dict__,
            "verdicts": [v.__dict__ for v in verdicts],
            "runtime_node": RUNTIME_NODE_ID,
        }
        ev = Evidence(
            evidence_id=str(uuid.uuid4()), node_id=RUNTIME_NODE_ID,
            issued_at=int(time.time() * 1000), lamport_clock=self.clock,
            prev_hash=self.ledger.head_hash, payload_hash=hash_payload(payload),
            payload=payload)
        return self.ledger.append(ev)

    async def handle_client(self, websocket):
        try:
            async for raw in websocket:
                try:
                    event = Event.from_json(json.loads(raw))
                    verdicts = self.rules.evaluate(event.__dict__)
                    ev = self.write_evidence(event, verdicts)
                    print(f"[runtime] {event.event_type} node={event.node_id} evidence={ev.evidence_id[:8]}")
                except (json.JSONDecodeError, KeyError, ValueError) as exc:
                    print(f"[runtime] rejected event: {exc}")
        except websockets.ConnectionClosed:
            pass

    async def run(self):
        print(f"[runtime] listening on {WS_HOST}:{WS_PORT}")
        async with websockets.serve(self.handle_client, WS_HOST, WS_PORT):
            while not self._shutdown:
                await asyncio.sleep(0.25)

def main():
    runtime = Runtime()
    def stop(signum, _frame):
        print(f"[runtime] signal {signum}; stopping")
        runtime._shutdown = True
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    asyncio.run(runtime.run())

if __name__ == "__main__":
    main()
