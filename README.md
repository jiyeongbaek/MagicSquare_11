# MagicSquare 4x4 - TDD 개발 보드

## 1) 프로젝트 개요

이 프로젝트는 부분적으로 비어 있는 `4x4` 마방진을 완성하는 시스템을 TDD 방식으로 구현합니다.  
기준 문서(SSOT)는 `docs/PRD_4x4_MagicSquare_TDD.md`이며, 본 README의 To-Do는 해당 PRD를 기준으로 작성되었습니다.

- 목표: 정답 생성 자체보다 **불변조건(Invariant) 기반 검증/판정 설계** 훈련
- 범위: 입력 검증, 빈칸 탐지, 누락 숫자 탐색, 조합 판정, 오류 계약 고정
- 비범위: UI 렌더링 구현, DB, 네트워크 서버, N x N 일반화

### GUI 실행 (공식 진입점)

- `python -m magicsquare.gui`

---

## 2) 도메인 규칙 요약 (PRD 5장 기준)

- 보드는 항상 `4x4`이어야 함 (INV-01)
- `0`은 빈칸, 빈칸은 정확히 `2개`여야 함 (INV-02)
- 값은 `0` 또는 `1..16`만 허용 (INV-03)
- `0`을 제외한 숫자 중복 금지 (INV-04)
- 마방진 목표 합은 `34` (INV-05)
- 완성 판정은 모든 행/열/대각선 합이 `34` (INV-06)
- 출력은 `int[6] = [r1,c1,n1,r2,c2,n2]`, 좌표는 1-index (INV-07)

---

## 3) 아키텍처 (ECB)

`.cursorrules`를 준수하여 아래 역할을 유지합니다.

- **Boundary**
  - 입력/출력 형식 처리, 오류 코드 매핑
  - 비즈니스 규칙 직접 구현 금지
- **Control**
  - 검증 및 해결 흐름 오케스트레이션
  - 정순/역순 조합 평가, 실패 시 오류 반환
- **Entity**
  - 보드 상태와 도메인 규칙(불변조건) 표현

의존성 방향:

- `boundary -> control`
- `control -> entity`
- `entity -> (outward dependency 없음)`

---

## 4) TDD 워크플로우 (RED -> GREEN -> REFACTOR)

- **RED**
  - 실패 테스트 먼저 작성
  - 실패 원인이 목표 규칙 위반인지 확인
- **GREEN**
  - 테스트를 통과시키는 최소 코드만 구현
  - 불필요한 기능 추가 금지
- **REFACTOR**
  - 테스트 모두 통과 상태에서만 구조 개선
  - 입력/출력/오류 계약은 절대 변경 금지

---

## 5) To-Do 보드 (AC/UC 기반)

To-Do 설계 순서:

1. PRD `## 8` AC를 작업 단위로 분해
2. PRD `## 7` UC로 흐름 그룹핑
3. PRD `## 5` INV로 누락 점검
4. PRD `## 11` Traceability로 Test/Code 연결
5. PRD `## 4.2` 성공 기준으로 DoD 설정
6. PRD `## 9`로 RED/GREEN/REFACTOR 순서 통제

### Epic / User Story / Requirement 매핑

- **Epic-001**: 마방진 검증 및 완성 시스템 구현
- **US-001 (REQ-001)**: 유효한 입력에서 빈칸 2개를 채워 `int[6]` 결과를 반환한다.
- **US-002 (REQ-002)**: 유효하지 않은 입력에서 허용된 오류 코드로만 실패를 반환한다.
- **US-003 (REQ-003)**: 모든 규칙은 Scenario -> Test -> Code로 추적 가능해야 한다.
- **US-004 (REQ-004)**: ECB 계층을 준수하고 Boundary에 비즈니스 규칙을 두지 않는다.

### 진행 상태 정의

- `[ ] TODO`: 아직 시작하지 않음
- `[~] DOING`: 현재 진행 중
- `[x] DONE`: 테스트 통과 및 코드 반영 완료
- `[!] BLOCKED`: 선행 작업 미완료 또는 설계 이슈

### Phase A - RED (실패 테스트 먼저)

- [ ] **TASK-001 | RED | REQ-001 | 보드 생성 실패 테스트(크기 검증)**
  - Scenario Level: L2
  - Scenario: `4x4`가 아닌 입력을 주면 즉시 거부한다.
  - Test: `test_board_creation_rejects_non_4x4_matrix`
  - Code Target: `entity/models/board.py`
  - ECB: Entity
  - 선행조건: 없음
  - 완료조건: `E_MATRIX_SIZE` 실패가 재현되고 테스트가 의도대로 실패
  - 체크포인트: UC-01, INV-01, AC-01

- [ ] **TASK-002 | RED | REQ-001 | 값 범위 실패 테스트**
  - Scenario Level: L3
  - Scenario: `0` 또는 `1..16` 범위를 벗어난 값이 포함되면 거부한다.
  - Test: `test_board_rejects_out_of_range_values`
  - Code Target: `entity/rules/value_range_rule.py`
  - ECB: Entity
  - 선행조건: TASK-001
  - 완료조건: `E_VALUE_RANGE` 실패 테스트가 의도된 assertion으로 실패
  - 체크포인트: UC-01, INV-03, AC-01

- [ ] **TASK-003 | RED | REQ-001 | 중복 숫자 실패 테스트**
  - Scenario Level: L3
  - Scenario: `0` 제외 숫자 중복이 존재하면 거부한다.
  - Test: `test_board_rejects_duplicate_nonzero_values`
  - Code Target: `entity/rules/uniqueness_rule.py`
  - ECB: Entity
  - 선행조건: TASK-001
  - 완료조건: `E_DUPLICATE_NONZERO` 실패 테스트가 재현
  - 체크포인트: UC-01, INV-04, AC-01

- [ ] **TASK-004 | RED | REQ-001 | 빈칸 개수 실패 테스트**
  - Scenario Level: L3
  - Scenario: 빈칸(`0`) 개수가 정확히 2개가 아니면 거부한다.
  - Test: `test_validate_input_rejects_invalid_blank_count`
  - Code Target: `control/services/input_validator.py`
  - ECB: Control
  - 선행조건: TASK-001
  - 완료조건: `E_BLANK_COUNT`가 정확히 반환되도록 실패 테스트 확보
  - 체크포인트: UC-01, INV-02, AC-01

- [ ] **TASK-005 | RED | REQ-001 | 빈칸 탐지 실패 테스트(row-major)**
  - Scenario Level: L1
  - Scenario: 빈칸 좌표를 row-major 순서로 2개 반환한다.
  - Test: `test_find_blank_cells_returns_two_positions_row_major`
  - Code Target: `control/services/blank_cell_finder.py`
  - ECB: Control
  - 선행조건: TASK-004
  - 완료조건: 반환 순서가 고정되어야 하며 테스트가 현재 구현에서 실패
  - 체크포인트: UC-02, AC-02

- [ ] **TASK-006 | RED | REQ-001 | 후보값 필터링 실패 테스트(누락 숫자)**
  - Scenario Level: L1
  - Scenario: 누락 숫자 2개를 오름차순 `[small, large]`로 반환한다.
  - Test: `test_find_missing_numbers_returns_sorted_pair`
  - Code Target: `control/services/missing_number_finder.py`
  - ECB: Control
  - 선행조건: TASK-002, TASK-003
  - 완료조건: 후보 숫자 계산/정렬을 검증하는 테스트가 실패
  - 체크포인트: UC-03, AC-02

- [ ] **TASK-007 | RED | REQ-001 | 완성 로직 실패 테스트(정순 우선)**
  - Scenario Level: L1
  - Scenario: `small->first, large->second` 조합이 유효하면 즉시 채택한다.
  - Test: `test_resolver_prefers_forward_combination_when_valid`
  - Code Target: `control/services/combination_resolver.py`
  - ECB: Control
  - 선행조건: TASK-005, TASK-006
  - 완료조건: 정순 우선 규칙을 검증하는 테스트가 실패
  - 체크포인트: UC-05, AC-03

- [ ] **TASK-008 | RED | REQ-001 | 완성 로직 실패 테스트(역순 fallback)**
  - Scenario Level: L2
  - Scenario: 정순 실패 시 역순 조합을 평가하여 성공하면 채택한다.
  - Test: `test_resolver_falls_back_to_reverse_combination`
  - Code Target: `control/services/combination_resolver.py`
  - ECB: Control
  - 선행조건: TASK-007
  - 완료조건: fallback 경로가 테스트로 재현되고 실패 상태 확인
  - 체크포인트: UC-05, AC-03

- [ ] **TASK-009 | RED | REQ-002 | 해결 불가 실패 테스트**
  - Scenario Level: L3
  - Scenario: 두 조합 모두 실패하면 `E_NO_VALID_COMBINATION` 반환
  - Test: `test_resolver_raises_no_valid_combination`
  - Code Target: `control/services/combination_resolver.py`
  - ECB: Control
  - 선행조건: TASK-007, TASK-008
  - 완료조건: 정확한 오류 코드로 실패 테스트가 작성됨
  - 체크포인트: UC-05, AC-03

- [ ] **TASK-010 | RED | REQ-002 | Boundary 오류 코드 화이트리스트 테스트**
  - Scenario Level: L2
  - Scenario: Boundary가 허용 목록 외 코드 반환을 차단한다.
  - Test: `test_boundary_returns_whitelisted_error_codes_only`
  - Code Target: `boundary/api/error_mapper.py`
  - ECB: Boundary
  - 선행조건: TASK-004, TASK-009
  - 완료조건: 화이트리스트 검증 테스트가 실패 상태로 작성
  - 체크포인트: UC-07, AC-04

- [ ] **TASK-011 | RED | REQ-001 | 출력 계약 실패 테스트(`int[6]`, 1-index)**
  - Scenario Level: L2
  - Scenario: 성공 응답이 `int[6]` 포맷과 1-index 좌표를 준수한다.
  - Test: `test_solver_output_matches_int6_schema`
  - Code Target: `boundary/api/response_mapper.py`
  - ECB: Boundary
  - 선행조건: TASK-007
  - 완료조건: 출력 계약 위반 시 테스트가 실패
  - 체크포인트: UC-05/07, INV-07, AC-03

### Phase B - GREEN (최소 구현으로 통과)

- [ ] **TASK-012 | GREEN | REQ-001 | Board Entity 최소 구현**
  - Scenario Level: L0
  - 연결 테스트: TASK-001~004
  - Code Target: `entity/models/board.py`, `entity/rules/*.py`
  - ECB: Entity
  - 선행조건: RED 테스트 4개 존재
  - 완료조건: RED 테스트 전부 통과, 신규 기능 확장 없음

- [ ] **TASK-013 | GREEN | REQ-004 | Control 입력 검증 오케스트레이션 구현**
  - Scenario Level: L1
  - 연결 테스트: `test_validate_input_*`, TASK-010
  - Code Target: `control/services/input_validator.py`, `control/use_cases/solve_magic_square.py`
  - ECB: Control
  - 선행조건: TASK-012
  - 완료조건: Boundary 호출 없이 Control이 검증/흐름 조율

- [ ] **TASK-014 | GREEN | REQ-001 | 빈칸 탐지 + 후보값 필터링 구현**
  - Scenario Level: L1
  - 연결 테스트: TASK-005, TASK-006
  - Code Target: `control/services/blank_cell_finder.py`, `control/services/missing_number_finder.py`
  - ECB: Control
  - 선행조건: TASK-012
  - 완료조건: row-major 및 오름차순 규칙 통과

- [ ] **TASK-015 | GREEN | REQ-001 | 완성 로직 구현(정순->역순)**
  - Scenario Level: L1
  - 연결 테스트: TASK-007~009
  - Code Target: `control/services/combination_resolver.py`, `entity/rules/magic_sum_rule.py`
  - ECB: Control/Entity
  - 선행조건: TASK-014
  - 완료조건: 성공/실패 분기 모두 통과, `E_NO_VALID_COMBINATION` 고정

- [ ] **TASK-016 | GREEN | REQ-002 | Boundary 입출력/오류 계약 구현**
  - Scenario Level: L2
  - 연결 테스트: TASK-010, TASK-011
  - Code Target: `boundary/api/request_validator.py`, `boundary/api/response_mapper.py`, `boundary/api/error_mapper.py`
  - ECB: Boundary
  - 선행조건: TASK-013, TASK-015
  - 완료조건: Boundary 계층에서 비즈니스 계산 없음

### Phase C - REFACTOR (행동 불변, 구조 개선)

- [ ] **TASK-017 | REFACTOR | REQ-002 | 오류 코드/메시지 상수화**
  - Scenario Level: L2
  - 연결 테스트: `test_error_message_contract_is_fixed`
  - Code Target: `control/constants/error_codes.py`, `boundary/api/error_mapper.py`
  - ECB: Control/Boundary
  - 선행조건: TASK-016
  - 완료조건: 코드/메시지 계약 문자열 완전 고정

- [ ] **TASK-018 | REFACTOR | REQ-004 | ECB 의존성 경계 정리**
  - Scenario Level: L0
  - 연결 테스트: `test_boundary_does_not_import_entity_directly`
  - Code Target: `boundary/**`, `control/**`, `entity/**`
  - ECB: Boundary/Control/Entity
  - 선행조건: TASK-016
  - 완료조건: `boundary -> control -> entity` 위배 import 0건

- [ ] **TASK-019 | REFACTOR | REQ-003 | 테스트 중복 제거 및 이름 일관화**
  - Scenario Level: L0
  - 연결 테스트: 전체 회귀 테스트
  - Code Target: `tests/**`
  - ECB: 테스트 자산
  - 선행조건: TASK-016
  - 완료조건: 테스트 의미 유지 + 중복 fixture 축소

### Phase D - 품질 게이트/릴리스 체크

- [ ] **TASK-020 | GREEN | REQ-003 | Domain Logic 커버리지 95%+ 확인**
  - Scenario Level: L2
  - 연결 테스트: `pytest --cov`
  - Code Target: `tests/control/**`, `tests/entity/**`
  - ECB: Control/Entity
  - 선행조건: TASK-019
  - 완료조건: Domain coverage >= 95%
  - 체크포인트: PRD 4.2 성공 기준 충족

- [ ] **TASK-021 | GREEN | REQ-002 | 입력/출력/오류 계약 테스트 100% 확인**
  - Scenario Level: L2/L3
  - 연결 테스트: 계약 테스트 스위트(`test_contract_input_*`, `test_contract_output_*`, `test_contract_error_*`)
  - Code Target: `tests/boundary/**`, `tests/integration/**`
  - ECB: Boundary/Integration
  - 선행조건: TASK-016
  - 완료조건: 계약 테스트 실패 0건
  - 체크포인트: AC-01~AC-04 완전 통과

- [ ] **TASK-022 | GREEN | REQ-003 | Traceability 완결성 검증**
  - Scenario Level: L0
  - 연결 테스트: `test_traceability_rows_have_test_links`
  - Code Target: `docs/traceability.md` 또는 README 추적 표
  - ECB: 문서/품질 게이트
  - 선행조건: TASK-021
  - 완료조건: AC/UC/INV -> TASK/Test/Code 연결 누락 0건

### 빠른 실행 순서 (권장)

- [ ] `A-RED`: TASK-001 -> 011 순서 완료
- [ ] `B-GREEN`: TASK-012 -> 016 순서 완료
- [ ] `C-REFACTOR`: TASK-017 -> 019 순서 완료
- [ ] `D-GATE`: TASK-020 -> 022 순서 완료

---

## 6) 추적성 (Traceability)

아래 매핑을 기본 규칙으로 유지합니다.

- `AC-01` -> 입력 검증 테스트군 -> `InputValidator`, `Board`
- `AC-02` -> 좌표/누락 숫자 테스트군 -> `BlankCellFinder`, `MissingNumberFinder`
- `AC-03` -> 조합/판정 테스트군 -> `CombinationResolver`, `MagicSquareJudge`
- `AC-04` -> 오류 계약 테스트군 -> `ErrorMapper`
- `AC-05` -> 운영 계약 테스트군 -> 운영 게이트 컴포넌트

또한 PRD `## 11`의 Concept-to-Code Traceability Matrix를 기준으로 각 TASK의 Test/Code 연결을 유지합니다.

---

## 7) 개발 규칙 (.cursorrules 반영)

- Python `3.10+`, PEP8 준수, 최대 줄 길이 `88`
- 모든 함수 파라미터/리턴 타입 힌트 필수
- public 메서드 Google 스타일 docstring 필수
- 테스트 프레임워크는 `pytest`, 테스트 이름은 `test_` 접두사
- 금지: `print()`, bare `except`, 비즈니스 로직 하드코딩 상수

---

## 8) 완료 기준 (Definition of Done)

- AC-01~AC-05가 모두 테스트 가능 형태로 구현/검증됨
- UC-01~UC-08이 최소 1개 이상의 테스트와 연결됨
- INV-01~INV-07이 성공/실패 시나리오로 검증됨
- 출력 계약 `int[6]` + 1-index 좌표가 항상 보장됨
- 오류 코드는 화이트리스트(`E_*`) 내에서만 반환됨
- Domain Logic 커버리지 `95%` 이상
- RED -> GREEN -> REFACTOR 순서를 모든 기능 작업에 적용함

---

## 9) 문서 참조

- SSOT: `docs/PRD_4x4_MagicSquare_TDD.md`
- 개발 규칙: `.cursorrules`
