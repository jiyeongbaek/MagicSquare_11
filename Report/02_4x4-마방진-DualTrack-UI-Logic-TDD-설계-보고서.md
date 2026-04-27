# Magic Square (4x4) — Dual-Track UI + Logic TDD 설계 보고서

## 문서 목적 및 고정 계약

- 목적: 알고리즘 난이도보다 **레이어 분리 + 계약 기반 테스트 + 리팩토링** 훈련
- 구현 코드: 작성하지 않음 (설계/계약/테스트/통합 계획만)
- UI 정의: 실제 화면이 아닌 입력/출력 경계(Boundary)
- Data 정의: DB가 아닌 저장/로드 인터페이스(메모리/파일 교체 가능)

### 입력 계약 (고정)

- 타입: `4x4 int[][]` (`0`은 빈칸)
- 빈칸 개수: 정확히 `2`
- 값 범위: `0` 또는 `1~16`
- 중복 규칙: `0` 제외 중복 금지

### 출력 계약 (고정)

- 타입: `int[6]`
- 좌표: `1-index`
- 형식: `[r1,c1,n1,r2,c2,n2]`
- 규칙: `n1,n2`는 두 누락 숫자이며  
  `(작은수->첫빈칸, 큰수->둘째빈칸)` 조합이 마방진이면 그 순서, 아니면 반대 순서

---

# 1) Logic Layer (Domain Layer) 설계

## 1.1 도메인 개념

| 분류 | 이름 | 책임(SRP) | 비고 |
|---|---|---|---|
| Entity | MagicSquareCandidate | 4x4 상태와 좌표 기반 값 조회 | 상태 표현 전용 |
| Value Object | CellPosition | 1-index 좌표 `(r,c)` 유효성 보장 | `1~4` 범위 강제 |
| Value Object | MissingNumbers | 누락 숫자 2개(오름차순) 보관 | 중복 불가 |
| Domain Service | InputValidator | 입력 계약 검증 | 실패 시 오류 코드 반환 |
| Domain Service | BlankCellFinder | 빈칸 2개 위치 추출 | 순서: 행 우선 |
| Domain Service | MissingNumberFinder | `1~16` 대비 누락 숫자 2개 계산 | `0` 제외 |
| Domain Service | MagicSquareJudge | 행/열/대각선 합 판정 | 상수 `34` 기준 |
| Domain Service | CombinationResolver | 두 숫자 배치 조합 시험 후 결과 결정 | 출력 포맷 생성 |

## 1.2 도메인 불변조건(Invariants)

| ID | Invariant | 검증 규칙(테스트 가능) | 실패 코드 |
|---|---|---|---|
| INV-D-01 | 행렬 크기 | 행 4개, 각 행 열 4개 | E_MATRIX_SIZE |
| INV-D-02 | 빈칸 수 | 값 `0`의 개수 == 2 | E_BLANK_COUNT |
| INV-D-03 | 값 범위 | 각 셀은 `0` 또는 `1~16` | E_VALUE_RANGE |
| INV-D-04 | 중복 | `0` 제외 중복 금지 | E_DUPLICATE_NONZERO |
| INV-D-05 | 매직 상수 | 목표 합 = `34` | E_MAGIC_CONSTANT |
| INV-D-06 | 완성 판정 | 모든 행/열/대각선 합이 `34` | E_NOT_MAGIC |
| INV-D-07 | 출력 형식 | `int[6]` / 좌표 1-index / `n1,n2`는 누락 숫자 | E_OUTPUT_FORMAT |

## 1.3 핵심 유스케이스(도메인 관점)

| UC | 설명 | 입력 | 출력 | 주요 실패 |
|---|---|---|---|---|
| UC-D-01 | 빈칸 찾기 | 4x4 matrix | `[(r1,c1),(r2,c2)]` | E_BLANK_COUNT |
| UC-D-02 | 누락 숫자 찾기 | 4x4 matrix | `[small, large]` | E_DUPLICATE_NONZERO |
| UC-D-03 | 마방진 판정 | 완성된 4x4 matrix | `true/false` | E_NOT_MAGIC |
| UC-D-04 | 두 조합 시도 | `blankPos + [small,large]` | `[r1,c1,n1,r2,c2,n2]` | E_NO_VALID_COMBINATION |

## 1.4 Domain API(내부 계약)

| API 시그니처(코드 아님) | 입력 | 출력 | 실패조건 |
|---|---|---|---|
| `validateInput(matrix: int[][])` | 4x4 int[][] | `ValidationResult{ok,errorCode}` | INV-D-01~04 위반 |
| `findBlankCells(matrix: int[][])` | 검증 통과 matrix | `CellPosition[2]` | 빈칸 2개 아님 |
| `findMissingNumbers(matrix: int[][])` | 검증 통과 matrix | `MissingNumbers{small,large}` | 중복/범위 위반 |
| `isMagic(matrix: int[][])` | 4x4 int[][](0 없음) | boolean | 행렬 크기 위반 |
| `resolveTwoCombinations(matrix: int[][])` | 검증 통과 matrix(0 두 개) | `int[6]=[r1,c1,n1,r2,c2,n2]` | 두 조합 모두 실패 시 E_NO_VALID_COMBINATION |

### 조합 규칙 고정

- small을 첫 빈칸, large를 둘째 빈칸에 넣은 결과가 마방진이면 그 순서를 채택
- 아니면 반대 순서를 채택
- 두 순서 모두 실패하면 도메인 실패 처리

## 1.5 Domain 단위 테스트 설계(RED 우선)

| 테스트 ID | 케이스 | 기대 결과 | 보호 Invariant |
|---|---|---|---|
| T-D-RED-01 | 3x4 입력 | E_MATRIX_SIZE | INV-D-01 |
| T-D-RED-02 | 빈칸 1개 | E_BLANK_COUNT | INV-D-02 |
| T-D-RED-03 | 빈칸 3개 | E_BLANK_COUNT | INV-D-02 |
| T-D-RED-04 | 값 17 포함 | E_VALUE_RANGE | INV-D-03 |
| T-D-RED-05 | 값 -1 포함 | E_VALUE_RANGE | INV-D-03 |
| T-D-RED-06 | 0 제외 중복(예: 5 두 번) | E_DUPLICATE_NONZERO | INV-D-04 |
| T-D-RED-07 | 정상 입력에서 빈칸 좌표 추출 | 1-index 좌표 2개 | INV-D-07 |
| T-D-RED-08 | 정상 입력에서 누락 숫자 추출 | `[small,large]` 오름차순 | INV-D-04 |
| T-D-RED-09 | 조합 A가 성공 | A 순서 결과 반환 | INV-D-06, INV-D-07 |
| T-D-RED-10 | 조합 A 실패/B 성공 | B 순서 결과 반환 | INV-D-06, INV-D-07 |
| T-D-RED-11 | 두 조합 모두 실패 | E_NO_VALID_COMBINATION | INV-D-06 |

### Domain RED 체크리스트

- [ ] 모든 입력 오류는 고정 오류 코드로 귀결된다.
- [ ] `INV-D-01 ~ INV-D-07` 각각을 직접 보호하는 테스트가 1개 이상 존재한다.
- [ ] 조합 규칙(정순/역순)이 테스트로 고정된다.
- [ ] 출력 배열 길이와 좌표 인덱스 규칙이 테스트로 고정된다.

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)

## 2.1 사용자/호출자 관점 시나리오

| 단계 | 행동 | 검증/처리 | 산출 |
|---|---|---|---|
| S1 | 4x4 행렬 입력 | Schema 검증 | 요청 수락 또는 오류 |
| S2 | Boundary 검증 통과 | Domain use case 호출 | Domain 응답 수신 |
| S3 | Domain 성공 | Output schema 검증 | `int[6]` 반환 |
| S4 | Domain/검증 실패 | Error schema 매핑 | 표준 오류 반환 |

## 2.2 UI 계약(외부 계약)

| 계약 | 정의 | 검증 규칙 |
|---|---|---|
| Input schema | `matrix: int[4][4]` | 0은 정확히 2개, 값은 0 또는 1~16, 0 제외 중복 금지 |
| Output schema | `result: int[6]` | `[r1,c1,n1,r2,c2,n2]`, r/c는 1~4, n1/n2는 누락 숫자 2개 |
| Error schema | `{code, message, details?}` | code는 사전 정의 집합만 허용 |

## 2.3 UI 레벨 테스트(Contract-first, RED 우선)

> Domain은 Mock으로 가정

| 테스트 ID | 입력 | Domain Mock | 기대 |
|---|---|---|---|
| T-UI-RED-01 | 행 3개 | 호출되지 않음 | E_MATRIX_SIZE 반환 |
| T-UI-RED-02 | 빈칸 1개 | 호출되지 않음 | E_BLANK_COUNT 반환 |
| T-UI-RED-03 | 값 18 포함 | 호출되지 않음 | E_VALUE_RANGE 반환 |
| T-UI-RED-04 | 0 제외 중복 | 호출되지 않음 | E_DUPLICATE_NONZERO 반환 |
| T-UI-RED-05 | 정상 입력 | 성공 int[6] 반환 | 출력 포맷 일치 |
| T-UI-RED-06 | 정상 입력 | 도메인 실패(E_NO_VALID_COMBINATION) | 오류 매핑 정확성 |
| T-UI-RED-07 | 정상 입력 | 잘못된 길이 배열 반환 | E_OUTPUT_FORMAT 반환 |

## 2.4 UX/출력 규칙

| 규칙 ID | 규칙 | 정확한 문구 규칙(검증 가능) |
|---|---|---|
| UX-01 | 오류 응답 구조 | 항상 `code`, `message` 포함; `details`는 선택 |
| UX-02 | 메시지 고정 | 코드별 `message`는 상수 문자열로 고정 |
| UX-03 | 내부 정보 보호 | stack trace, 파일경로, 예외 원문 노출 금지 |
| UX-04 | 성공 응답 구조 | 항상 `result` 필드에 `int[6]`만 포함 |
| UX-05 | 언어 일관성 | `message`는 한국어만 사용 |

### Error Message 표준

| Error Code | Message(고정 문자열) |
|---|---|
| E_MATRIX_SIZE | 입력 행렬 크기는 4x4여야 합니다. |
| E_BLANK_COUNT | 빈칸(0)의 개수는 정확히 2개여야 합니다. |
| E_VALUE_RANGE | 각 셀의 값은 0 또는 1~16이어야 합니다. |
| E_DUPLICATE_NONZERO | 0을 제외한 숫자는 중복될 수 없습니다. |
| E_OUTPUT_FORMAT | 출력 형식이 int[6] 계약과 일치하지 않습니다. |
| E_NO_VALID_COMBINATION | 두 숫자 배치 조합 모두 마방진 조건을 만족하지 않습니다. |
| E_DATA_LOAD_FAILED | 저장된 입력을 불러오지 못했습니다. |
| E_DATA_SAVE_FAILED | 실행 결과를 저장하지 못했습니다. |

### UI RED 체크리스트

- [ ] 검증 실패 입력은 Domain 호출 이전에 차단된다.
- [ ] 성공 경로에서 Output schema 검증이 항상 수행된다.
- [ ] Domain 오류 코드가 UI Error schema로 일관되게 매핑된다.
- [ ] Error message는 고정 문자열과 정확히 일치한다.

---

# 3) Data Layer 설계 (Data Layer)

## 3.1 목적 정의

- 학습 범위의 저장/로드만 담당
- 알고리즘 계산 로직은 포함하지 않음
- 저장 대상
  - 입력 행렬
  - 실행 결과 `int[6]` (선택)

## 3.2 인터페이스 계약

| 인터페이스 | 메서드 시그니처(코드 아님) | 입력 | 출력 | 실패 |
|---|---|---|---|---|
| MatrixRepository | `saveInput(runId: string, matrix: int[][])` | runId, 4x4 matrix | void | E_DATA_SAVE_FAILED |
| MatrixRepository | `loadInput(runId: string)` | runId | int[][] | E_DATA_LOAD_FAILED |
| ResultRepository | `saveResult(runId: string, result: int[6])` | runId, int[6] | void | E_DATA_SAVE_FAILED |
| ResultRepository | `loadResult(runId: string)` | runId | int[6] | E_DATA_LOAD_FAILED |

## 3.3 구현 옵션 비교(메모리/파일)

| 옵션 | 장점 | 단점 | 적합 상황 |
|---|---|---|---|
| 옵션 A: InMemory | 빠르고 단순, 테스트 속도 우수 | 프로세스 종료 시 데이터 소실 | 단위 테스트, TDD 루프 |
| 옵션 B: File(JSON/CSV) | 재시작 후 재현 가능 | I/O 실패/포맷 오류 처리 필요 | 통합 테스트, 회귀 재현 |

### 추천안

- 추천: **A(InMemory) + 통합 검증용 보조 어댑터로 B(File JSON)**
- 이유:
  - TDD 반복 속도를 유지
  - 실패 재현 시 파일 스냅샷 활용 가능

## 3.4 Data 레이어 테스트

| 테스트 ID | 케이스 | 기대 결과 | 보호 규칙 |
|---|---|---|---|
| T-DA-01 | `saveInput` 후 `loadInput` | 동일 4x4 행렬 | 저장/로드 정합성 |
| T-DA-02 | `saveResult` 후 `loadResult` | 동일 int[6] | 저장/로드 정합성 |
| T-DA-03 | 존재하지 않는 runId 로드 | E_DATA_LOAD_FAILED | 예외 매핑 |
| T-DA-04 | 파일 형식 손상(JSON 오류) | E_DATA_LOAD_FAILED | 형식 오류 처리 |
| T-DA-05 | 4x4 아닌 데이터 저장 시도 | 저장 거부 | INV-D-01 유지 |
| T-DA-06 | int[6] 아닌 결과 저장 시도 | 저장 거부 | INV-D-07 유지 |

### Data RED 체크리스트

- [ ] 저장/로드 왕복 테스트가 타입별로 존재한다.
- [ ] 파일 없음/형식 오류 예외가 고정 코드로 매핑된다.
- [ ] 데이터 계층에서 입력/출력 불변조건 위반을 저장 전에 차단한다.

---

# 4) Integration & Verification (통합 및 검증)

## 4.1 통합 경로 정의

| 경로 | 설명 | 의존성 방향 |
|---|---|---|
| UI -> Application | 입력 스키마 검증 후 유스케이스 호출 | UI는 Application 인터페이스에만 의존 |
| Application -> Domain | 도메인 조합 해석 수행 | Application은 Domain 계약에 의존 |
| Application -> Data | 입력/결과 저장 및 로드 | Domain은 Data를 모름 |
| Domain (독립) | 불변조건/판정 로직 보유 | 외부 레이어 의존 없음 |

## 4.2 통합 테스트 시나리오

| ID | 유형 | 시나리오 | 기대 결과 |
|---|---|---|---|
| T-INT-01 | 정상 | 유효 입력 + 조합 A 성공 | int[6] 반환, Data 저장 성공 |
| T-INT-02 | 정상 | 유효 입력 + 조합 A 실패/B 성공 | 역순 배치 int[6] 반환 |
| T-INT-03 | 실패(입력) | 빈칸 3개 입력 | UI에서 E_BLANK_COUNT, Domain 미호출 |
| T-INT-04 | 실패(도메인) | 두 조합 모두 실패 케이스 | E_NO_VALID_COMBINATION |
| T-INT-05 | 실패(데이터) | saveResult I/O 실패 | E_DATA_SAVE_FAILED 매핑 |
| T-INT-06 | 실패(데이터) | loadInput 파일 없음 | E_DATA_LOAD_FAILED 매핑 |

## 4.3 회귀 보호 규칙

| 규칙 ID | 정책 | 검증 방법 |
|---|---|---|
| REG-01 | 기존 테스트 유지 정책: 테스트 삭제 금지 | CI에서 테스트 수 감소 시 실패 |
| REG-02 | 입력 계약 변경 금지 | Contract 테스트 스냅샷 비교 |
| REG-03 | 출력 포맷 변경 금지(`int[6]`) | 응답 스키마 테스트 고정 |
| REG-04 | Error code 집합 변경 금지(승인 없이는 불가) | 에러 코드 화이트리스트 테스트 |
| REG-05 | 도메인 불변조건 완화 금지 | Invariant 테스트 전수 통과 필수 |

## 4.4 커버리지 목표

| 레이어 | 목표 | 게이트 조건 |
|---|---|---|
| Domain Logic | 95%+ | 라인/브랜치 둘 다 95% 미만이면 실패 |
| UI Boundary | 85%+ | 입출력/에러 계약 테스트 필수 포함 |
| Data | 80%+ | 정상/예외 경로 모두 포함 |

## 4.5 Traceability Matrix (필수)

| Concept(Invariant) | Rule | Use Case | Contract | Test | Component |
|---|---|---|---|---|---|
| INV-D-01 | 4x4 크기 고정 | UC-D-01 | Input schema | T-D-RED-01, T-UI-RED-01 | InputValidator |
| INV-D-02 | 빈칸 2개 | UC-D-01 | Input schema | T-D-RED-02/03, T-UI-RED-02 | BlankCellFinder |
| INV-D-03 | 값 범위 | UC-D-02 | Input schema | T-D-RED-04/05, T-UI-RED-03 | InputValidator |
| INV-D-04 | 0 제외 중복 금지 | UC-D-02 | Input schema | T-D-RED-06, T-UI-RED-04 | MissingNumberFinder |
| INV-D-06 | 마방진 합 34 | UC-D-03/04 | Domain API | T-D-RED-09/10/11 | MagicSquareJudge |
| INV-D-07 | int[6] 출력 계약 | UC-D-04 | Output schema | T-UI-RED-05/07, T-DA-06 | CombinationResolver |
| E_DATA_LOAD_FAILED | 로드 실패 매핑 | 통합 로드 | Error schema | T-DA-03/04, T-INT-06 | Repository Adapter |
| E_DATA_SAVE_FAILED | 저장 실패 매핑 | 통합 저장 | Error schema | T-INT-05 | Repository Adapter |

### 통합 검증 체크리스트

- [ ] 정상 시나리오 2개 이상 존재한다.
- [ ] 실패 시나리오 3개 이상 존재한다.
- [ ] 계약/출력 포맷 변경 방지 테스트가 CI 게이트에 연결되어 있다.
- [ ] Traceability Matrix의 모든 행이 실제 테스트 ID로 연결된다.

---

## 문서 준수 확인

- [x] 모호한 표현(적절히/충분히) 미사용
- [x] 모든 규칙을 테스트 항목으로 검증 가능하게 정의
- [x] 구현 코드 미포함
- [x] 표/체크리스트 중심 구성
