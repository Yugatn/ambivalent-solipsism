# Assurance runner

Expected semantic outcomes:
- AntiReplay_Protocol.tla: PASS
- AntiReplay_Broken.tla: EXPECTED_COUNTEREXAMPLE

The broken model is a negative control. Its success criterion is a real TLC invariant violation, not merely a non-zero process exit.

The runner requires TLA2TOOLS_JAR and records TLC output for evidence generation. Claims are not promoted automatically.