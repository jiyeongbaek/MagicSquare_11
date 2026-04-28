# To-do list creation references
_Exported on 4/28/2026 at 11:00:05 GMT+9 from Cursor (3.2.11)_

---

**User**

to-do 리스트를 작성하고 싶습니다. 작성한 문서 중 무엇을 참조해서 만들어야 할까요?


---

**Cursor**

요청하신 목적(실행 가능한 to-do 리스트 작성)에 맞춰, 현재 문서에서 바로 참조할 섹션을 빠르게 확인한 뒤 가장 효율적인 기준을 추천드리겠습니다.

to-do 리스트는 지금 문서 기준으로는 `docs/PRD_4x4_MagicSquare_TDD.md` 하나를 **기준 문서(SSOT)**로 삼으면 됩니다.  
특히 아래 순서로 참조하면 가장 깔끔합니다.

- `## 8. 테스트 가능한 인수 기준(AC)` → to-do의 **직접 작업 단위**로 분해하기 좋음
- `## 7. 유스케이스 정의` → 기능 흐름(UC-01~08) 기준으로 묶기 좋음
- `## 5. 핵심 개념과 불변조건` → 누락 방지 체크리스트(INV-01~07)
- `## 11. Traceability Matrix` → 각 to-do를 테스트 ID/컴포넌트와 연결
- `## 4.2 측정 가능한 성공 기준` → 완료 정의(Definition of Done)
- `## 9. TDD 실행 원칙` → 작업 순서(RED→GREEN→REFACTOR) 관리

실무적으로는 **“AC 기준으로 to-do 생성 → UC로 그룹핑 → INV/Traceability로 누락 점검”** 방식이 가장 안전합니다.  
원하시면 제가 이 문서 기준으로 바로 실행 가능한 to-do 리스트 초안(체크박스 형식)까지 만들어드릴게요.

---

**User**

당신은 시니어 소프트웨어 아키텍트이자 TDD 코치입니다. 할 일 목록의 항목과 완료 조건은 아래와 같아.
 to-do 리스트는 docs/PRD_4x4_MagicSquare_TDD.md 하나를 **기준 문서(SSOT)**로 삼아줘.
특히 아래 순서로 참조해.
## 8. 테스트 가능한 인수 기준(AC) → to-do의 직접 작업 단위로 분해하기 좋음
## 7. 유스케이스 정의 → 기능 흐름(UC-01~08) 기준으로 묶기 좋음
## 5. 핵심 개념과 불변조건 → 누락 방지 체크리스트(INV-01~07)
## 11. Traceability Matrix → 각 to-do를 테스트 ID/컴포넌트와 연결
## 4.2 측정 가능한 성공 기준 → 완료 정의(Definition of Done)
## 9. TDD 실행 원칙 → 작업 순서(RED→GREEN→REFACTOR) 관리

다음 방법론을 적용하여
"Magic Square 4x4 완성 시스템"의 구현용 To-Do 구조를 작성하세요.
적용 방법론:
Concept-to-Code Traceability
Dual-Track UI + Logic TDD
To-Do → Scenario → Test → Code 구조
ECB(Entity / Control / Boundary) 모델
RED → GREEN → REFACTOR
반드시 한국어로 작성하세요.
[시스템 목표]
부분적으로 비어 있는 4x4 Magic Square를 완성하는 시스템의 개발 To-Do를 작성합니다.
[도메인 규칙]
보드는 4x4이다.
숫자는 1~16만 사용한다.
0은 빈칸이다.
정확히 2칸이 비어 있다.
0을 제외한 중복 숫자는 허용되지 않는다.
모든 행, 열, 대각선의 합은 34여야 한다.
해결 가능한 경우 빈칸 값을 찾아 채운다.
유효하지 않은 보드는 거부한다.
[출력 형식]
다음 구조를 반드시 지켜서 작성하세요.
Epic
User Story
Phase별 Task 목록
각 Task에는 반드시 아래 정보를 포함하세요.
Task ID
RED / GREEN / REFACTOR 여부
작업 제목
Scenario Level (L0/L1/L2/L3)
연결되는 Test 이름
연결되는 Code 대상
ECB 스테레오타입 (Entity / Control / Boundary)
필요 시 체크포인트
[표현 스타일]
Markdown 사용
체크박스 형식 사용
실제 Cursor.AI 실습용 개발 보드처럼 작성
식별자는 Epic-001, US-001, TASK-001 형식 사용
유효한 케이스와 실패 케이스를 모두 포함
최소한 다음 작업을 포함
보드 생성
보드 유효성 검사
빈칸 탐지
후보값 필터링
완성 로직
잘못된 입력 처리
테스트 커버리지 체크포인트
[Scenario Level 정의]
L0: 기능 개요
L1: 정상 흐름
L2: 경계 상황
L3: 실패 상황
[추가 제약]
Logic 책임은 명확히 분리할 것
UI/Boundary에는 비즈니스 규칙을 넣지 말 것
Control은 검증과 해결 흐름을 조율할 것
Entity는 보드 상태를 표현할 것
모든 To-Do는 Scenario, Test, Code로 추적 가능해야 함
이제
"Magic Square 4x4 완성 시스템"의 To-Do 구조를 생성하세요.

---

**Cursor**

## SSOT 및 참조 원칙

- 기준 문서(SSOT): `docs/PRD_4x4_MagicSquare_TDD.md`
- 참조 우선순위:
  1. `## 8. 테스트 가능한 인수 기준(AC)`
  2. `## 7. 유스케이스 정의(UC-01~08)`
  3. `## 5. 핵심 개념/불변조건(INV-01~07)`
  4. `## 11. Traceability Matrix`
  5. `## 4.2 측정 가능한 성공 기준`
  6. `## 9. TDD 실행 원칙(RED→GREEN→REFACTOR)`

---

## Epic-001: Magic Square 4x4 완성 시스템 구현

### User Story

- **US-001**: 사용자로서, 유효한 `4x4` 보드를 입력하면 시스템이 빈칸 2개를 규칙에 맞게 채운 결과를 받고 싶다.
- **US-002**: 사용자로서, 잘못된 입력이면 표준 오류 코드(`E_*`)로 일관된 실패 응답을 받고 싶다.
- **US-003**: 개발팀으로서, 모든 요구사항이 `To-Do → Scenario → Test → Code`로 추적 가능하길 원한다.
- **US-004**: 코치/리뷰어로서, Dual-Track(UI/Boundary + Logic) TDD와 ECB 경계가 깨지지 않길 원한다.

---

## Phase 1) RED (실패 테스트 먼저 작성)

### US-001 / 보드 생성 & 기본 규칙

- [ ] **TASK-001 (RED)**
  - **작업 제목**: `4x4` 보드 엔티티 생성 규칙 실패 테스트 작성
  - **Scenario Level**: L2
  - **연결 Test 이름**: `test_board_creation_rejects_non_4x4_matrix` (Trace: T-D-RED-01)
  - **연결 Code 대상**: `entity/models/board.py`
  - **ECB 스테레오타입**: Entity
  - **체크포인트**: INV-01 위반 시 `E_MATRIX_SIZE`로 귀결되는 실패 경로 확인

- [ ] **TASK-002 (RED)**
  - **작업 제목**: 값 범위 위반(`0` 또는 `1..16` 외 값) 실패 테스트 작성
  - **Scenario Level**: L3
  - **연결 Test 이름**: `test_board_rejects_out_of_range_values` (Trace: T-D-RED-04)
  - **연결 Code 대상**: `entity/rules/value_range_rule.py`
  - **ECB 스테레오타입**: Entity
  - **체크포인트**: INV-03 커버

- [ ] **TASK-003 (RED)**
  - **작업 제목**: `0` 제외 중복 숫자 실패 테스트 작성
  - **Scenario Level**: L3
  - **연결 Test 이름**: `test_board_rejects_duplicate_nonzero_values` (Trace: T-D-RED-06)
  - **연결 Code 대상**: `entity/rules/uniqueness_rule.py`
  - **ECB 스테레오타입**: Entity
  - **체크포인트**: INV-04 커버

### US-002 / 입력 검증(Boundary-Track)

- [ ] **TASK-004 (RED)**
  - **작업 제목**: Boundary 입력 스키마 실패 테스트 작성(크기 오류)
  - **Scenario Level**: L3
  - **연결 Test 이름**: `test_boundary_returns_e_matrix_size_for_invalid_shape` (Trace: T-UI-RED-01)
  - **연결 Code 대상**: `boundary/api/request_validator.py`
  - **ECB 스테레오타입**: Boundary
  - **체크포인트**: Boundary는 검증 호출/매핑만 수행(비즈니스 규칙 금지)

- [ ] **TASK-005 (RED)**
  - **작업 제목**: Boundary 빈칸 개수 오류 실패 테스트 작성(2개 아님)
  - **Scenario Level**: L3
  - **연결 Test 이름**: `test_boundary_returns_e_blank_count_when_not_two_blanks` (Trace: T-UI-RED-02)
  - **연결 Code 대상**: `boundary/api/request_validator.py`
  - **ECB 스테레오타입**: Boundary
  - **체크포인트**: INV-02/AC-01 매핑

- [ ] **TASK-006 (RED)**
  - **작업 제목**: 허용 오류코드 화이트리스트 실패 테스트 작성
  - **Scenario Level**: L2
  - **연결 Test 이름**: `test_boundary_error_code_is_in_whitelist_only`
  - **연결 Code 대상**: `boundary/api/error_mapper.py`
  - **ECB 스테레오타입**: Boundary
  - **체크포인트**: `E_*` 외 코드 반환 금지(AC-04)

### US-001 / 빈칸 탐지·후보값·완성 로직(Control/Entity-Track)

- [ ] **TASK-007 (RED)**
  - **작업 제목**: row-major 빈칸 탐지 실패 테스트 작성
  - **Scenario Level**: L1
  - **연결 Test 이름**: `test_find_blank_cells_returns_two_positions_in_row_major` (Trace: T-D-RED-03)
  - **연결 Code 대상**: `control/services/blank_cell_finder.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: UC-02, INV-02

- [ ] **TASK-008 (RED)**
  - **작업 제목**: 누락 숫자 오름차순 추출 실패 테스트 작성
  - **Scenario Level**: L1
  - **연결 Test 이름**: `test_find_missing_numbers_returns_sorted_pair` (Trace: T-D-RED-05)
  - **연결 Code 대상**: `control/services/missing_number_finder.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: 후보값 필터링 시작점

- [ ] **TASK-009 (RED)**
  - **작업 제목**: 정순 조합 우선 평가 실패 테스트 작성
  - **Scenario Level**: L1
  - **연결 Test 이름**: `test_resolver_prefers_forward_combination_when_valid` (Trace: T-D-RED-09)
  - **연결 Code 대상**: `control/services/combination_resolver.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: AC-03 정순 성공 규칙

- [ ] **TASK-010 (RED)**
  - **작업 제목**: 정순 실패/역순 성공 fallback 실패 테스트 작성
  - **Scenario Level**: L2
  - **연결 Test 이름**: `test_resolver_falls_back_to_reverse_combination` (Trace: T-D-RED-10)
  - **연결 Code 대상**: `control/services/combination_resolver.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: AC-03 fallback 규칙

- [ ] **TASK-011 (RED)**
  - **작업 제목**: 두 조합 모두 실패 시 오류 반환 테스트 작성
  - **Scenario Level**: L3
  - **연결 Test 이름**: `test_resolver_raises_e_no_valid_combination_when_both_fail` (Trace: T-D-RED-11)
  - **연결 Code 대상**: `control/services/combination_resolver.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: `E_NO_VALID_COMBINATION` 고정

- [ ] **TASK-012 (RED)**
  - **작업 제목**: 완성 보드 합 34 판정 실패 테스트 작성(행/열/대각선)
  - **Scenario Level**: L2
  - **연결 Test 이름**: `test_magic_square_judge_validates_sum_34_for_all_lines`
  - **연결 Code 대상**: `entity/rules/magic_sum_rule.py`
  - **ECB 스테레오타입**: Entity
  - **체크포인트**: INV-05/INV-06

---

## Phase 2) GREEN (최소 구현으로 테스트 통과)

- [ ] **TASK-013 (GREEN)**
  - **작업 제목**: Board 엔티티 최소 구현(4x4/값/중복/빈칸 2개)
  - **Scenario Level**: L0
  - **연결 Test 이름**: TASK-001~003 대응 테스트
  - **연결 Code 대상**: `entity/models/board.py`, `entity/rules/*.py`
  - **ECB 스테레오타입**: Entity
  - **체크포인트**: Entity는 상태/도메인 규칙만 보유

- [ ] **TASK-014 (GREEN)**
  - **작업 제목**: 입력 검증 Control 오케스트레이션 구현
  - **Scenario Level**: L1
  - **연결 Test 이름**: `test_validate_input_returns_ok_for_valid_board`, RED 테스트군
  - **연결 Code 대상**: `control/services/input_validator.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: Control은 검증 흐름 조율, Boundary/Entity 분리 유지

- [ ] **TASK-015 (GREEN)**
  - **작업 제목**: 빈칸 탐지 + 후보값 필터링(누락 숫자) 최소 구현
  - **Scenario Level**: L1
  - **연결 Test 이름**: TASK-007, TASK-008 대응 테스트
  - **연결 Code 대상**: `control/services/blank_cell_finder.py`, `control/services/missing_number_finder.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: row-major, 오름차순 유지

- [ ] **TASK-016 (GREEN)**
  - **작업 제목**: 완성 로직(정순→역순) 및 결과 `int[6]` 포맷 구현
  - **Scenario Level**: L1
  - **연결 Test 이름**: TASK-009~011 + `test_solver_returns_int6_output_format` (Trace: T-UI-RED-05)
  - **연결 Code 대상**: `control/use_cases/solve_magic_square.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: 출력 `[r1,c1,n1,r2,c2,n2]`, 1-index 강제(INV-07)

- [ ] **TASK-017 (GREEN)**
  - **작업 제목**: Boundary 응답 매핑 구현(성공/오류 계약)
  - **Scenario Level**: L2
  - **연결 Test 이름**: TASK-004~006 대응 테스트
  - **연결 Code 대상**: `boundary/api/response_mapper.py`, `boundary/api/error_mapper.py`
  - **ECB 스테레오타입**: Boundary
  - **체크포인트**: Boundary에 비즈니스 판단 로직 금지

---

## Phase 3) REFACTOR (구조 개선, 계약 불변)

- [ ] **TASK-018 (REFACTOR)**
  - **작업 제목**: 에러 코드/메시지 상수화 및 단일 소스 정리
  - **Scenario Level**: L2
  - **연결 Test 이름**: `test_error_messages_match_fixed_contract_exactly`
  - **연결 Code 대상**: `control/constants/error_codes.py`, `boundary/api/error_mapper.py`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: AC-04 고정 문자열 일치

- [ ] **TASK-019 (REFACTOR)**
  - **작업 제목**: ECB 의존성 점검 리팩터링(불법 import 제거)
  - **Scenario Level**: L0
  - **연결 Test 이름**: `test_architecture_boundary_does_not_import_entity_directly`
  - **연결 Code 대상**: `boundary/**`, `control/**`, `entity/**`
  - **ECB 스테레오타입**: Boundary/Control/Entity
  - **체크포인트**: `boundary -> control -> entity` 단방향 유지

- [ ] **TASK-020 (REFACTOR)**
  - **작업 제목**: Traceability 태깅 보강(테스트-코드-요구 연결 주석/메타)
  - **Scenario Level**: L0
  - **연결 Test 이름**: `test_traceability_matrix_rows_map_to_at_least_one_test`
  - **연결 Code 대상**: `tests/**`, `docs/traceability.md`(선택)
  - **ECB 스테레오타입**: Control
  - **체크포인트**: PRD `##11` 행 단위 추적 가능

---

## Phase 4) 품질 게이트/완료 조건(DoD) 체크

- [ ] **TASK-021 (GREEN)**
  - **작업 제목**: 커버리지 게이트 검증
  - **Scenario Level**: L2
  - **연결 Test 이름**: `pytest --cov` 기반 품질 파이프라인 테스트
  - **연결 Code 대상**: `tests/control/**`, `tests/entity/**`, `pyproject.toml` 또는 `pytest.ini`
  - **ECB 스테레오타입**: Control
  - **체크포인트**: Domain Logic 커버리지 `95%` 이상(성공 기준 4.2)

- [ ] **TASK-022 (GREEN)**
  - **작업 제목**: 입력/출력/오류 계약 100% 통과 검증
  - **Scenario Level**: L1/L3
  - **연결 Test 이름**: 계약 테스트 스위트(`test_contract_input_*`, `test_contract_output_*`, `test_contract_error_*`)
  - **연결 Code 대상**: `tests/boundary/**`, `tests/integration/**`
  - **ECB 스테레오타입**: Boundary
  - **체크포인트**: 입력/출력/화이트리스트 오류코드 테스트 100%

- [ ] **TASK-023 (GREEN)**
  - **작업 제목**: 실패/지연/품질 운영 게이트 시나리오 검증(MLOps Track)
  - **Scenario Level**: L2/L3
  - **연결 Test 이름**: `test_ops_alert_triggered_on_threshold_breach` (Trace: T-OPS-RED-06)
  - **연결 Code 대상**: `control/services/alert_evaluator.py`(또는 운영 계약 목 구현)
  - **ECB 스테레오타입**: Control
  - **체크포인트**: UC-08 및 PRD AC-05 연결

---

## 시나리오 보드 (To-Do → Scenario → Test → Code 요약)

- [ ] **정상 흐름(L1)**: 유효한 4x4 + 빈칸2개 + 조합 성공 → `int[6]` 반환  
  - Test: `test_solver_returns_int6_output_format`  
  - Code: `control/use_cases/solve_magic_square.py`

- [ ] **경계 흐름(L2)**: 정순 실패 후 역순 성공  
  - Test: `test_resolver_falls_back_to_reverse_combination`  
  - Code: `control/services/combination_resolver.py`

- [ ] **실패 흐름(L3)**: 크기 오류/범위 오류/중복/빈칸 수 오류/해결 불가  
  - Test: `test_boundary_returns_e_matrix_size_for_invalid_shape`, `test_resolver_raises_e_no_valid_combination_when_both_fail`  
  - Code: `boundary/api/error_mapper.py`, `control/services/input_validator.py`

---

## 완료 정의(Definition of Done)

- [ ] 모든 AC(AC-01~AC-05)에 대해 최소 1개 이상 테스트가 존재한다.
- [ ] UC-01~UC-08이 테스트/코드에 매핑되어 Traceability 공백이 없다.
- [ ] INV-01~INV-07이 각각 실패/성공 테스트로 검증된다.
- [ ] Boundary 계층에 비즈니스 규칙이 없고, Control이 흐름 조율을 담당한다.
- [ ] Entity는 보드 상태와 도메인 규칙 표현에 집중한다.
- [ ] RED→GREEN→REFACTOR 순서를 모든 기능 단위에서 준수한다.
- [ ] 성공 기준: Domain coverage 95%+, 계약 테스트 100% 통과.

원하면 다음 단계로, 이 보드를 바로 실행 가능한 형태로 `tests/`와 `src/` 초기 파일 트리(ECB 구조)까지 같이 쪼개서 드리겠습니다.

---

**User**

To-do 리스트를  포함해 READMD.md 파일을 만들고 싶습니다. 무슨 문서를 참조하면 좋을까요?


---

**Cursor**

`README.md`(질문에선 `READMD.md`)를 만들 때는 아래 2개를 우선 참조하면 충분합니다.

- **필수(SSOT)**: `docs/PRD_4x4_MagicSquare_TDD.md`
  - To-do 항목의 기준은 이 문서에서 가져오세요.
  - 특히 순서대로:
    1) `## 8. 테스트 가능한 인수 기준(AC)`  
    2) `## 7. 유스케이스 정의`  
    3) `## 5. 핵심 개념/불변조건`  
    4) `## 11. Traceability Matrix`  
    5) `## 4.2 측정 가능한 성공 기준`  
    6) `## 9. TDD 실행 원칙`

- **구현/규칙 보조**: `.cursorrules`
  - ECB 계층 규칙, TDD 규칙, 테스트/코딩 스타일을 README의 “개발 규칙” 섹션에 반영하기 좋습니다.

추천 구조는 다음처럼 잡으면 깔끔합니다:
- 프로젝트 개요
- 도메인 규칙 요약(PRD 5장)
- 아키텍처(ECB)
- TDD 워크플로우(RED→GREEN→REFACTOR)
- **To-do 보드**(AC/UC 기반)
- 추적성(Traceability 링크)
- 완료 기준(DoD)

원하시면 제가 지금 바로 `README.md` 초안을 만들어 드릴게요.

---

**User**

 To-Do 리스트를 포함한 MagicSquare를 만들기 위한 README.md 파일을 만들어줘.
아래 2개를 우선 참조하면 충분합니다.

필수(SSOT): docs/PRD_4x4_MagicSquare_TDD.md

To-do 항목의 기준은 이 문서에서 가져오세요.
특히 순서대로:
## 8. 테스트 가능한 인수 기준(AC)
## 7. 유스케이스 정의
## 5. 핵심 개념/불변조건
## 11. Traceability Matrix
## 4.2 측정 가능한 성공 기준
## 9. TDD 실행 원칙
구현/규칙 보조: .cursorrules

ECB 계층 규칙, TDD 규칙, 테스트/코딩 스타일을 README의 “개발 규칙” 섹션에 반영하기 좋습니다.
추천 구조는 다음처럼 잡으면 깔끔합니다:

프로젝트 개요
도메인 규칙 요약(PRD 5장)
아키텍처(ECB)
TDD 워크플로우(RED→GREEN→REFACTOR)
To-do 보드(AC/UC 기반)
추적성(Traceability 링크)
완료 기준(DoD)


---

**Cursor**

요청하신 구조와 기준 문서(SSOT)를 그대로 반영해서 `README.md`를 새로 작성하겠습니다. 먼저 기존 `README.md` 유무를 확인한 뒤, PRD와 `.cursorrules` 기준으로 To-Do 포함 버전을 생성하겠습니다.

이제 `README.md`를 새로 생성해서, 요청하신 섹션 구조(개요/도메인/ECB/TDD/To-Do/Traceability/DoD)와 AC→UC 기반 작업 보드를 한 번에 반영하겠습니다.

`README.md`를 새로 생성했고, 요청하신 기준을 모두 반영했습니다.

- 생성 파일: `README.md`
- 반영 내용:
  - SSOT 기준 명시: `docs/PRD_4x4_MagicSquare_TDD.md`
  - 섹션 구조: 프로젝트 개요 / 도메인 규칙 / ECB / TDD 워크플로우 / To-Do 보드 / Traceability / 개발 규칙 / DoD
  - To-Do 보드: 체크박스 형식, `Epic-001`, `US-001`, `TASK-001~021`
  - 각 Task에 포함:
    - RED/GREEN/REFACTOR
    - Scenario Level(L0~L3)
    - 연결 Test
    - 연결 Code 대상
    - ECB 스테레오타입
    - 체크포인트(필요 항목)
  - 유효/실패 케이스 모두 포함
  - 최소 필수 항목(보드 생성, 유효성 검사, 빈칸 탐지, 후보값 필터링, 완성 로직, 잘못된 입력 처리, 커버리지 체크포인트) 포함
  - `.cursorrules` 기반 개발 규칙 반영

원하시면 다음으로 `README.md`의 To-Do ID를 실제 `tests/` 파일명/테스트 함수명 규칙과 1:1로 맞춘 실행 템플릿까지 바로 이어서 만들어드릴게요.

---

**User**

@README.md 파일 중 to-do list를 작성해줘. 자세하게 생각해서..

---

**Cursor**

요청하신 대로 `README.md`의 To-Do 섹션을 더 실행 가능한 수준으로 상세화하겠습니다. 먼저 현재 To-Do 구간을 확인한 뒤, 단계/추적성/체크포인트를 강화해서 바로 실습 가능한 보드 형태로 수정하겠습니다.

현재 To-Do는 좋지만 “실행 순서/완료판정/요구사항 추적”이 더 촘촘하면 실습성이 높아집니다. `## 5) To-Do 보드`를 상세 실행보드 형태(REQ-ID, 선행조건, 완료조건, 하위 단계)로 개편하겠습니다.

`README.md`의 To-Do 섹션을 요청하신 대로 **상세 실행보드 형태**로 개편했습니다.

변경 핵심:
- `## 5) To-Do 보드`를 전면 상세화
- **Epic / User Story / REQ-ID** 연결 추가
- 각 Task에 다음 항목을 모두 포함:
  - Task ID
  - RED/GREEN/REFACTOR
  - 작업 제목
  - Scenario Level (L0~L3)
  - Scenario 설명
  - 연결 Test
  - 연결 Code 대상
  - ECB 스테레오타입
  - 선행조건
  - 완료조건
  - 체크포인트(AC/UC/INV 매핑)
- **Phase A~D**(RED, GREEN, REFACTOR, Gate) 순서로 정렬
- 마지막에 **빠른 실행 순서 체크리스트** 추가

수정 파일:
- `README.md`

원하시면 다음으로 `TASK-001~022`를 실제 `tests/` 파일 템플릿(파일명/함수명까지)으로 자동 생성 가능한 스캐폴딩 목록도 바로 만들어드리겠습니다.

---

**User**

지금까지 작업한 내용 Report 폴더 안에 보고서로 만들어줘. 

---

**Cursor**

요청하신 대로 지금까지 진행한 작업을 요약한 보고서를 `Report` 폴더에 생성하겠습니다. 먼저 폴더 존재 여부를 확인하고, 없으면 보고서 파일 생성과 함께 정리본을 작성하겠습니다.

`Report` 폴더 기준으로 새 보고서를 추가하겠습니다. 이번 보고서에는 지금까지의 의사결정, 생성/수정 산출물, To-Do 보드 고도화 내역, 다음 액션을 한 번에 정리하겠습니다.

요청하신 보고서를 `Report` 폴더에 생성했습니다.

- 생성 파일: `Report/06_MagicSquare_진행작업_보고서.md`
- 포함 내용:
  - SSOT/보조문서 기반 작업 원칙
  - 지금까지 수행한 문서 작업 이력
  - `README.md` 생성 및 To-Do 고도화 상세
  - 산출물 목록
  - 정합성/품질 점검 결과
  - 현재 상태 평가 및 다음 권장 액션

원하시면 이어서 `Report/07_...`로 **Task별 실제 테스트 스캐폴딩 계획서**도 바로 만들어드리겠습니다.

