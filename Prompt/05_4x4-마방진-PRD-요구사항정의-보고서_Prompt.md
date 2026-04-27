# PRD structure for Magic Square project
_Exported on 4/27/2026 at 17:27:19 GMT+9 from Cursor (3.2.11)_

---

**User**

당신은 시니어 제품/소프트웨어 아키텍트이며 Dual-Track UI + Logic TDD 및 Concept-to-Code Traceability 전문가입니다.
PRD 본문 골격은 Report/4를 축으로 하고, Report/1로 문제·동기를 보강하며, 기능·계약·성공 정의는 Report/2, 품질·개발 원칙은 Report/3(및 cursor 규칙) 에서 가져오는 방식으로 다음 내용을 고려해 docs 폴더에 PRD를 작성해 주세요.

프로젝트: Magic Square (4x4) — TDD 연습용
목적:
알고리즘 난이도보다 TDD 훈련이 목적
Invariant 기반 설계/검증 사고를 체득
입력/출력 계약을 명확히 고정
UI/DB/Web 의존성 없이 순수 로직 중심으로 구현 가능하게 PRD 작성
⚠️ 중요 규칙
구현 코드를 작성하지 마십시오.
새로운 기능을 추가하지 마십시오. (요구사항 범위 유지)
모호한 표현(“적절히”, “충분히” 등)을 사용하지 마십시오.
모든 요구사항은 테스트/검증 가능해야 합니다.
Dual-Track(경계/도메인) 분리를 문서 구조에 반영하십시오.
Concept → Rule → Use Case → Contract → Test → Component 추적성을 반드시 포함하십시오.
출력은 구조화된 Markdown으로 작성하십시오.


---

**Cursor**

요청하신 기준(Report/4 중심, Report/1·2·3 보강, Dual-Track 구조, 추적성 강제)을 반영해서 `docs`에 PRD를 새로 작성하겠습니다. 먼저 `Report` 문서들의 실제 파일명/내용을 확인한 뒤, 요구사항을 테스트 가능 문장으로 재구성해 바로 작성하겠습니다.

핵심 근거는 확인됐고, 지금 `Report/2`와 `Report/3`에서 기능 계약·품질 원칙을 추출해 PRD의 요구사항/검증 항목으로 고정하겠습니다. 이후 `docs`에 최종 마크다운 파일을 생성하겠습니다.

문서 초안을 바로 생성하겠습니다. `docs` 폴더를 만든 뒤, 요청하신 추적성(Concept→Rule→Use Case→Contract→Test→Component)과 Dual-Track 구조를 포함한 PRD를 작성합니다.

`docs` 폴더에 요청 조건을 반영한 PRD를 작성했습니다.

- 생성 파일: `docs/PRD_4x4_MagicSquare_TDD.md`
- 반영 기준:
  - `Report/4`를 본문 골격(목표, 여정 기반 요구, 검증 중심 구조)으로 사용
  - `Report/1`의 문제 인식/동기/Invariant 관점을 문제정의 섹션에 반영
  - `Report/2`의 기능/입출력 계약/오류 코드/유스케이스/추적성 요소 반영
  - `Report/3` 및 `.cursorrules`의 품질/ECB/TDD 원칙 반영
- 문서 특징:
  - Dual-Track 분리: `Boundary Track` / `Domain Track` 명시
  - Concept → Rule → Use Case → Contract → Test → Component 추적성 매트릭스 포함
  - 모호한 표현 없이 테스트 가능한 요구사항으로 작성
  - 구현 코드 및 범위 외 신규 기능 추가 없이 작성

원하시면 다음으로 이 PRD를 기준으로 `테스트 명세서(RED 단계 전용)` 문서도 `docs`에 분리해 드리겠습니다.

---

**User**

Report  폴더에 보고서로 내보내줘

---

**Cursor**

요청하신 대로 `docs`의 PRD를 `Report` 폴더용 보고서 파일로 그대로 내보내겠습니다. 파일명은 기존 규칙에 맞춰 `05_...-보고서.md` 형태로 생성하겠습니다.

`Report` 폴더로 내보냈습니다.

- 생성 파일: `Report/05_4x4-마방진-PRD-요구사항정의-보고서.md`
- 내용: `docs/PRD_4x4_MagicSquare_TDD.md`와 동일한 PRD 본문

원하시면 다음으로 `docs` 원본은 유지할지, 아니면 `Report` 버전만 남기고 정리할지도 맞춰드릴게요.

