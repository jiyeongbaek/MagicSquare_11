# PRD: Magic Square (4x4) — TDD Training Product Requirements

## 1. 문서 목적

- 이 문서는 `4x4` 마방진 문제를 **알고리즘 풀이 과제**가 아닌 **TDD 훈련 과제**로 정의한다.
- 요구사항의 목표는 정답 생성 자체가 아니라, 불변조건(Invariant) 기반 설계/검증 사고를 훈련하는 것이다.
- 본 PRD는 UI/DB/Web 구현 의존성 없이, 경계/도메인/운영 계약을 재현 가능하게 고정한다.

## 2. 배경 및 문제 정의

### 2.1 문제 배경

- 4x4 마방진은 제약 조건 충돌과 누락이 드러나기 쉬운 크기다.
- 결과 중심 접근은 "거의 맞음" 착시를 만든다.
- 학습 목표는 결과가 아니라 조건 판정 기준을 고정하고 재현하는 것이다.

### 2.2 최종 문제 정의

- 시스템은 부분적으로 채워진 `4x4` 격자 상태가 제약을 만족하는지 판별하고,
- 두 개 빈칸에 대한 배치 결과를 고정된 출력 계약으로 반환해야 한다.
- 제약 위반 시 사전 정의된 오류 코드로 실패를 보고해야 한다.

## 3. 범위(Scoped) / 비범위(Out of Scope)

### 3.1 범위

- 입력 계약 검증(크기/빈칸 수/값 범위/중복 규칙)
- 빈칸 좌표 탐색
- 누락 숫자 탐색
- 두 조합(정순/역순) 평가 및 결과 반환
- 마방진 판정(행/열/대각선 합)
- 오류 코드/메시지 계약 고정
- MLOps 계약 정의(데이터/모델 아티팩트/서빙/모니터링)

### 3.2 비범위

- UI 렌더링 구현(화면, 스타일, 상호작용)
- DB 저장/조회 구현
- 네트워크/API 서버 구현
- MLOps 인프라 실제 구축(CI/CD, 모델 레지스트리, 모니터링 도구)
- 일반화된 N x N 마방진 확장
- 빈칸 2개 초과 문제 해결

## 4. 제품 목표 및 성공 기준

### 4.1 제품 목표

- Invariant 기반 설계 사고를 훈련한다.
- Dual-Track(경계/도메인) TDD 흐름을 훈련한다.
- 운영 계약(Data/Serving/Monitoring) 기반 품질 게이트 설계를 훈련한다.
- 입력/출력 계약을 변경 불가 기준으로 고정한다.

### 4.2 측정 가능한 성공 기준

- Domain Logic 테스트 커버리지 `95%` 이상
- 입력 계약 테스트 `100%` 통과
- 출력 계약(`int[6]`, 1-index 좌표) 테스트 `100%` 통과
- 에러 코드 화이트리스트 테스트 `100%` 통과
- 추적성 매트릭스의 모든 행이 최소 1개 테스트 ID와 연결됨
- 데이터 계약 검증 테스트 `100%` 통과
- 서빙 계약(요청/응답 스키마, 오류 코드) 테스트 `100%` 통과
- 운영 게이트 기준선(지연/품질) 위반 시 배포 차단 규칙이 테스트로 검증됨

## 5. 핵심 개념과 불변조건(Invariants)

| ID | Invariant | 검증 규칙 |
|---|---|---|
| INV-01 | 격자 크기 고정 | 행 4개, 각 행 4열 |
| INV-02 | 빈칸 수 고정 | 값 `0`의 개수는 정확히 2개 |
| INV-03 | 값 범위 | 각 셀은 `0` 또는 `1..16` |
| INV-04 | 중복 규칙 | `0` 제외 중복 금지 |
| INV-05 | 마방진 상수 | 목표 합은 `34` |
| INV-06 | 완성 판정 | 모든 행/열/대각선 합이 `34` |
| INV-07 | 출력 형식 고정 | 결과는 `int[6]=[r1,c1,n1,r2,c2,n2]`, 좌표 1-index |

## 6. Tri-Track 요구사항 (Dual-Track + MLOps Track)

## 6.1 Boundary Track (입출력 계약 및 오류 매핑)

### 입력 계약

- 타입: `matrix: int[4][4]`
- 의미: `0`은 빈칸
- 빈칸: 정확히 2개
- 값 범위: `0` 또는 `1..16`
- 중복: `0` 제외 중복 금지

### 출력 계약

- 성공 타입: `result: int[6]`
- 포맷: `[r1,c1,n1,r2,c2,n2]`
- 좌표 규칙: `r1,c1,r2,c2`는 `1..4`
- 값 규칙: `n1,n2`는 누락된 두 숫자

### 오류 계약

- 타입: `{code, message, details?}`
- `code` 허용 집합:
  - `E_MATRIX_SIZE`
  - `E_BLANK_COUNT`
  - `E_VALUE_RANGE`
  - `E_DUPLICATE_NONZERO`
  - `E_OUTPUT_FORMAT`
  - `E_NO_VALID_COMBINATION`
- `message`는 코드별 고정 문자열로만 반환해야 한다.
- 오류 응답에는 내부 스택 정보, 파일 경로, 예외 원문을 포함하지 않는다.

## 6.2 Domain Track (순수 규칙 및 조합 판정)

### 고정 규칙

- 빈칸 좌표는 row-major 순서로 찾는다.
- 누락 숫자는 오름차순 `[small, large]`로 계산한다.
- 조합 평가 순서:
  1. `small -> first blank`, `large -> second blank`
  2. 1이 실패하면 반대 순서 평가
- 첫 성공 조합을 출력으로 채택한다.
- 두 조합 모두 실패하면 `E_NO_VALID_COMBINATION`을 반환한다.

## 6.3 MLOps Track (파이프라인/서빙/모니터링 계약)

### 데이터 계약(Data Contract)

- 학습/추론 입력 스키마는 `matrix: int[4][4]`로 고정한다.
- 값 범위/중복/빈칸 규칙(INV-02~04) 위반 데이터는 파이프라인에서 실패 처리한다.
- 데이터 검증 실패는 배포 후보 생성 단계로 진행하지 않는다.

### 모델/아티팩트 계약(Model Artifact Contract)

- 모델 버전은 고유 버전 식별자와 함께 기록되어야 한다.
- 학습 파라미터/평가 지표/데이터 버전은 재현 가능하도록 함께 저장되어야 한다.
- 기준선(metric baseline) 미달 모델은 배포 승인을 받을 수 없다.

### 서빙 계약(Serving Contract)

- 추론 API는 입력/출력/오류 코드를 Boundary Track 계약과 동일하게 유지해야 한다.
- 서빙 계층은 `E_*` 오류 코드 화이트리스트 외 값을 반환해서는 안 된다.
- 서빙 지연 목표를 위반하면 운영 경고 이벤트를 발생시켜야 한다.

### 모니터링 계약(Monitoring Contract)

- 입력 데이터 품질 이상(범위/형식 위반률 임계치 초과)을 감지해야 한다.
- 실패율/지연/품질 지표 임계치 초과 시 알림을 발행해야 한다.
- 알림 이벤트는 최소한 코드, 시각, 영향 지표를 포함해야 한다.

## 7. 유스케이스 정의

| Use Case ID | 이름 | 입력 | 출력 | 실패 코드 |
|---|---|---|---|---|
| UC-01 | 입력 검증 | `int[4][4]` | `ok` | `E_MATRIX_SIZE`, `E_BLANK_COUNT`, `E_VALUE_RANGE`, `E_DUPLICATE_NONZERO` |
| UC-02 | 빈칸 좌표 탐색 | 검증 통과 matrix | 좌표 2개(1-index) | `E_BLANK_COUNT` |
| UC-03 | 누락 숫자 탐색 | 검증 통과 matrix | `[small, large]` | `E_DUPLICATE_NONZERO`, `E_VALUE_RANGE` |
| UC-04 | 마방진 판정 | 완성된 matrix | `true/false` | `E_MATRIX_SIZE` |
| UC-05 | 두 조합 해결 | 검증 통과 matrix | `int[6]` | `E_NO_VALID_COMBINATION`, `E_OUTPUT_FORMAT` |
| UC-06 | 데이터 계약 검증 | 파이프라인 입력 데이터 | `pass/fail` | `E_MATRIX_SIZE`, `E_BLANK_COUNT`, `E_VALUE_RANGE`, `E_DUPLICATE_NONZERO` |
| UC-07 | 서빙 계약 검증 | 추론 요청 payload | 계약 일치 응답 | `E_OUTPUT_FORMAT`, `E_NO_VALID_COMBINATION` |
| UC-08 | 운영 알림 판정 | 지연/실패/품질 지표 스트림 | `alert/no-alert` | N/A |

## 8. 테스트 가능한 인수 기준(AC)

### AC-01 입력 검증

- `4x4`가 아니면 `E_MATRIX_SIZE`
- 빈칸 수가 2개가 아니면 `E_BLANK_COUNT`
- 범위를 벗어난 값이 있으면 `E_VALUE_RANGE`
- `0` 제외 중복이 있으면 `E_DUPLICATE_NONZERO`

### AC-02 좌표/숫자 탐색

- 빈칸 좌표 2개를 row-major 기준으로 반환
- 누락 숫자 2개를 오름차순으로 반환

### AC-03 조합 및 판정

- 정순 조합이 성공하면 정순 결과 반환
- 정순 실패/역순 성공이면 역순 결과 반환
- 두 조합 실패면 `E_NO_VALID_COMBINATION`
- 성공 결과는 항상 `int[6]` 포맷을 만족

### AC-04 오류 계약

- 모든 실패는 허용된 오류 코드 중 하나여야 한다.
- 코드별 메시지는 고정 문자열과 정확히 일치해야 한다.

### AC-05 MLOps 계약

- 데이터 스키마/규칙 위반 배치는 파이프라인 게이트에서 실패해야 한다.
- 기준선 미달 모델은 배포 후보로 승격되지 않아야 한다.
- 서빙 응답은 Boundary Track과 동일한 입출력/오류 계약을 유지해야 한다.
- 운영 지표 임계치 초과 시 알림 이벤트가 생성되어야 한다.

## 9. TDD 실행 원칙 (Gate)

### RED Gate

- 새 동작마다 실패 테스트를 먼저 작성한다.
- 실패 원인은 목표한 규칙 위반이어야 한다.

### GREEN Gate

- 실패 테스트를 통과시키는 최소 변경만 수행한다.
- 테스트 통과 확인 후 추가 기능을 넣지 않는다.

### REFACTOR Gate

- 모든 테스트가 통과한 상태에서만 구조를 정리한다.
- 외부 계약(입력/출력/오류 코드)을 변경하지 않는다.

## 10. 품질 원칙 및 아키텍처 제약

### ECB 계층 규칙

- `boundary -> control -> entity` 방향만 허용한다.
- boundary는 entity를 직접 참조하지 않는다.
- business decision은 control에서 수행한다.

### 코드/테스트 규칙(구현 시 준수)

- Python `3.10+`
- PEP8 엄수, 최대 줄 길이 `88`
- 함수 시그니처 타입 힌트 필수
- public 메서드 Google 스타일 docstring 필수
- pytest 사용, 테스트 명은 `test_` 접두사
- 금지: `print()`, bare `except`, 비즈니스 로직 하드코딩 상수

## 11. Concept-to-Code Traceability Matrix (필수)

| Concept | Rule | Use Case | Contract | Test | Component | Pipeline Stage |
|---|---|---|---|---|---|---|
| Invariant 중심 판정 | INV-01 (4x4) | UC-01 | Input schema size | T-D-RED-01, T-UI-RED-01 | InputValidator | Data Validation |
| Invariant 중심 판정 | INV-02 (빈칸 2개) | UC-01, UC-02 | Input blank count | T-D-RED-02/03, T-UI-RED-02 | BlankCellFinder | Data Validation |
| Invariant 중심 판정 | INV-03 (범위) | UC-01, UC-03, UC-06 | Input value range | T-D-RED-04/05, T-UI-RED-03, T-OPS-RED-01 | InputValidator | Data Validation |
| Invariant 중심 판정 | INV-04 (중복 금지) | UC-01, UC-03, UC-06 | Input uniqueness | T-D-RED-06, T-UI-RED-04, T-OPS-RED-02 | MissingNumberFinder | Data Validation |
| 재현 가능한 판정 | INV-06 (합 34) | UC-04, UC-05 | Domain rule contract | T-D-RED-09/10/11 | MagicSquareJudge | Offline Evaluation |
| 출력 계약 고정 | INV-07 (`int[6]`) | UC-05, UC-07 | Output schema | T-UI-RED-05/07, T-OPS-RED-03 | CombinationResolver | Serving Contract Test |
| 실패 재현성 | E_NO_VALID_COMBINATION | UC-05, UC-07 | Error schema | T-D-RED-11, T-UI-RED-06, T-OPS-RED-04 | CombinationResolver | Serving Contract Test |
| 운영 게이트 일관성 | MLOPS-01 (기준선 통과) | UC-07 | Model promotion gate | T-OPS-RED-05 | ReleaseGate | Model Registry |
| 운영 이상 감지 | MLOPS-02 (임계치 알림) | UC-08 | Monitoring alert contract | T-OPS-RED-06 | AlertEvaluator | Monitoring |

## 12. 릴리스 승인 기준 (문서 기준)

- 모든 요구사항 문장은 테스트 가능한 형태여야 한다.
- 모호한 표현(예: "적절히", "충분히")을 포함하지 않는다.
- PRD 범위를 넘어서는 요구사항을 포함하지 않는다.
- Tri-Track 구분(경계/도메인/운영)이 문서 내에서 명확해야 한다.
- Traceability Matrix가 Concept -> Rule -> Use Case -> Contract -> Test -> Component -> Pipeline Stage를 완결적으로 연결해야 한다.
- 운영 게이트(데이터 검증/모델 승격/서빙 계약/알림 계약) 요구사항이 최소 1개 이상 테스트와 연결되어야 한다.
