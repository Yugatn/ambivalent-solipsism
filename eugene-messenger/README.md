# Eugene Messenger

Eugene Messenger — отдельный инженерно-исследовательский проект внутри экосистемы «Амбивалентного Солипсизма».

Это не обещание готового защищённого мессенджера. Проект развивается через проверяемую цепочку:

**Принцип → Архитектура → Threat Model → Security Claim → Specification → Formal Model → Implementation → Conformance → Adversarial Test → Benchmark → Audit → Residual Risk**

## Первая вертикальная срезка

Первый инженерный milestone называется **Anti-Replay Assurance Artifact**.

Цель — получить один полностью трассируемый security claim, для которого существуют:
- формальная спецификация;
- корректная TLA+ модель;
- намеренно сломанная модель;
- counterexample от TLC;
- reference implementation;
- adversarial test;
- machine-readable registry;
- CI-проверка трассируемости.

Первый claim:

> Ранее принятый authenticated message не должен повторно вызывать state transition.

## Структура

    eugene-messenger/
      spec/
        AntiReplay.tla
        AntiReplay.cfg
        AntiReplay_Broken.tla
      tests/
        test_anti_replay.py
        test_replay_attack.py
      evidence/
        anti-replay/
          README.md
      .github/
        workflows/
          assurance.yml

## Границы первого этапа

В первой модели сознательно не реализуются UI, федерация, WASM plugins, production cryptography и полноценный transport stack.

Сначала проверяется одно свойство безопасности состояния. После получения доказательного вертикального среза аналогичная схема переносится на identity continuity, capability lifecycle, recovery и protocol security.

## Статусы

planned означает, что claim зарегистрирован, но доказательная цепочка ещё не завершена.
specified означает наличие явной спецификации.
model_checked означает, что модель проверена TLC.
conformant означает, что реализация соответствует спецификации в пределах определённого тестового oracle.
audited означает отдельную внешнюю проверку.

Наличие прототипа, теста или модели само по себе не означает доказанную безопасность.

## Domain prototype

The executable domain layer is under core/domain. It adds platform-independent FavoriteState, HLC ordering, normalized swipe semantics, ArchiveState and HiddenArchive session primitives. It deliberately does not claim model-checked assurance.
