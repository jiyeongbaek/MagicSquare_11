# 4x4 magic square TDD document contents
_Exported on 4/28/2026 at 10:17:17 GMT+9 from Cursor (3.2.11)_

---

**User**

@docs/PRD_4x4_MagicSquare_TDD.md 작성하려고 합니다. 들어가야 할 내용이 무엇인지 알려주세요.

---

**Cursor**

`docs/PRD_4x4_MagicSquare_TDD.md`에 맞춰 실제로 어떤 항목을 채우면 좋은지, 현재 문서 구조를 먼저 확인한 뒤 필수/권장 내용을 정리해드리겠습니다.

`docs/PRD_4x4_MagicSquare_TDD.md`에 들어가야 할 핵심은 이미 잘 잡혀 있고, 작성 시에는 아래 12개를 **빈틈 없이 채우는 것**이 중요합니다.

- **문서 목적**: 이 PRD가 왜 존재하는지(알고리즘 정답이 아니라 TDD 훈련 목적) 명확히 선언
- **배경/문제정의**: 어떤 문제를 어떤 입출력 계약으로 해결하는지 1~2문장으로 고정
- **범위/비범위**: 구현할 것과 안 할 것을 분리(특히 UI/DB/API/NxN 확장 제외 여부)
- **제품 목표 + 수치형 성공기준**: 커버리지, 계약 테스트 통과율처럼 측정 가능한 KPI
- **불변조건(Invariants)**: 크기, 빈칸 수, 값 범위, 중복, 합(34), 출력 포맷 등 절대 규칙
- **Dual-Track 요구사항**:
  - Boundary: 입력/출력/오류 코드 계약
  - Domain: 빈칸 탐색, 누락 숫자, 조합 평가 순서, 판정 규칙
- **유스케이스 테이블**: 각 UC별 입력, 출력, 실패 코드 매핑
- **인수기준(AC)**: 테스트 가능한 문장으로만 작성 (모호어 금지)
- **TDD Gate**: RED/GREEN/REFACTOR에서 허용되는 행동을 명시
- **품질/아키텍처 제약**: 계층 규칙(ECB), 언어/스타일/테스트 정책
- **추적성 매트릭스**: Concept → Rule → UseCase → Contract → Test → Component 연결
- **릴리스 승인 기준**: 문서 완성도 체크리스트(테스트 가능성, 범위 일치, 추적성 완결성)

작성 품질을 높이는 기준은 간단합니다:
- 모든 요구사항이 **테스트 케이스로 바로 변환 가능**해야 하고,
- 실패 시 **고정된 오류 코드**로 재현 가능해야 하며,
- 어떤 구현자가 읽어도 **동일한 결과를 만들 수 있게** 계약이 고정되어야 합니다.

원하시면 이 문서를 기준으로 바로 쓸 수 있는 **“작성용 템플릿 버전(값 비워진 형태)”**으로 정리해드릴게요.

---

**User**

첨부한 파일처럼 나는 Dual-Track UI + Logic TDD with MLOps 작업을 하고싶은데, 어떻게 생각해?

---

**Cursor**

방향 매우 좋습니다.  
특히 첨부하신 원칙처럼 **UI 테스트는 로직을 모르고, Logic 테스트는 UI를 모르게 분리**하면, 나중에 MLOps까지 붙여도 변경 영향이 작아집니다.

## 왜 잘 맞는지

- **Dual-Track TDD**가 이미 “계약(UX Contract) vs 규칙(Logic Rule)” 분리를 강제해서, 모델/파이프라인 교체 시 회귀를 잡기 쉽습니다.
- MLOps를 추가하면 “학습/서빙/모니터링”이 들어오는데, 이때도 UI·Logic 계약이 고정되어 있으면 운영 안정성이 올라갑니다.
- 지금 PRD 구조(불변조건, 오류코드, Traceability)와 궁합이 좋습니다.

## 한 가지 조정 포인트

- 이름은 실무적으로 **Dual-Track + Ops Track** 또는 **Tri-Track**으로 두는 걸 추천합니다.  
  (UI/Logic만 Dual-Track이고, MLOps는 운영 트랙이기 때문)

## 추천 구조 (실행 가능한 형태)

- **UI Track (Boundary)**  
  - 입력 검증, 에러 메시지/코드 노출, 결과 포맷 표시 테스트
  - 절대 금지: 내부 계산 규칙을 UI 테스트에 직접 검증
- **Logic Track (Control+Entity)**  
  - Invariant(4x4, 빈칸2, 범위, 중복, 합34), 조합 순서, 판정 규칙 테스트
  - 절대 금지: 렌더링/컴포넌트 의존
- **MLOps Track (Pipeline+Serving+Monitoring)**  
  - 데이터/피처 스키마 검증  
  - 모델 버전·아티팩트 재현성(학습 해시, 파라미터, 메트릭 기준선)  
  - 서빙 계약 테스트(입출력 JSON schema, latency budget)  
  - 운영 모니터링 테스트(드리프트/성능 저하 알림 조건)

## PRD에 바로 추가하면 좋은 항목

- `13. MLOps 요구사항`  
  - 데이터 계약, 모델 레지스트리 규칙, 배포 게이트(오프라인/온라인 기준)
- `14. MLOps 인수 기준(AC)`  
  - 예: “스키마 변경 시 파이프라인은 실패해야 한다”, “latency p95 < Xms”
- `15. End-to-End Traceability 확장`  
  - Concept → Rule → UseCase → Contract → Test → Component → **Pipeline Stage**

원하시면 제가 지금 문서(`docs/PRD_4x4_MagicSquare_TDD.md`)에 맞춰  
**Dual-Track + MLOps 확장 섹션 초안**을 바로 작성해드릴게요.

---

**User**

그렇다면 지금 작업한 PRD내용을 Dual-Track UI + Logic TDD with MLOps를 기반으로 정리해서 다시 알려줘.

---

**Cursor**

좋습니다. 지금 PRD를 **Dual-Track UI + Logic TDD with MLOps** 기준으로 재정리하면 아래 형태가 가장 깔끔합니다.

## PRD 재정리본 (권장)

### 1) 문서 목적
- 본 문서는 4x4 마방진을 **알고리즘 정답 문제**가 아니라 **TDD + 운영가능성(MLOps) 훈련 문제**로 정의한다.
- 목표는 정답 생성이 아니라, **계약(UX/API) + 규칙(도메인) + 운영(파이프라인)** 을 재현 가능하게 고정하는 것이다.

### 2) 문제 정의
- 입력: `int[4][4]` (`0`은 빈칸, 빈칸 정확히 2개)
- 처리: 두 빈칸에 누락 숫자를 넣어 마방진(합 34) 성립 여부 판정
- 출력: 성공 시 `int[6]=[r1,c1,n1,r2,c2,n2]` (1-index), 실패 시 표준 오류 객체

### 3) 범위 / 비범위
- **범위**: 입력검증, 빈칸/누락숫자 탐색, 조합평가, 오류코드, 테스트 추적성, MLOps 게이트
- **비범위**: UI 스타일링, DB, 외부 API 서버, 일반화된 NxN, 빈칸 2개 초과 해법

### 4) 핵심 불변조건 (Invariants)
- `INV-01` 크기: 4x4 고정  
- `INV-02` 빈칸: `0` 정확히 2개  
- `INV-03` 값 범위: `0` 또는 `1..16`  
- `INV-04` 중복: `0` 제외 중복 금지  
- `INV-05` 마방진 상수: 34  
- `INV-06` 완성 판정: 행/열/대각선 모두 34  
- `INV-07` 출력 포맷: `int[6]`, 좌표 1-index

---

## 5) Tri-Track 요구사항 (Dual-Track + MLOps)

### A. UI Track (Boundary Contract)
- 입력 오류가 있으면 코드별 고정 메시지를 표시한다.
- 성공 시 결과 포맷을 정확히 렌더링한다.
- UI 테스트는 내부 합산 로직/조합 규칙을 직접 검증하지 않는다.

### B. Logic Track (Domain Rule)
- row-major로 빈칸 2개 탐색
- 누락 숫자 `[small, large]` 오름차순 계산
- 평가 순서:
  1. `small -> blank1`, `large -> blank2`
  2. 실패 시 반대 조합
- 첫 성공 조합을 채택, 둘 다 실패면 `E_NO_VALID_COMBINATION`
- Logic 테스트는 UI 표현을 검증하지 않는다.

### C. MLOps Track (Pipeline/Serving/Monitoring Contract)
- **Data Contract**: 입력 스키마/범위 위반 시 파이프라인 실패
- **Model/Artifact Contract**: 버전, 파라미터, 메트릭 기준선 기록 및 재현 가능
- **Serving Contract**: API 입출력 스키마, 에러코드, latency budget 준수
- **Monitoring Contract**: 품질 저하/드리프트 임계치 초과 시 알림

---

## 6) 오류 계약 (공통)
- 타입: `{code, message, details?}`
- 허용 코드:
  - `E_MATRIX_SIZE`
  - `E_BLANK_COUNT`
  - `E_VALUE_RANGE`
  - `E_DUPLICATE_NONZERO`
  - `E_OUTPUT_FORMAT`
  - `E_NO_VALID_COMBINATION`
- `message`는 코드별 고정 문자열만 허용, 내부 예외/스택 노출 금지

---

## 7) 인수기준(AC) 재구성

- **AC-UI-01**: 입력 오류별 고정 메시지 노출
- **AC-UI-02**: 성공 시 `int[6]` 구조/좌표 범위 표시 보장
- **AC-LOGIC-01**: 모든 Invariant 위반 케이스가 정확한 코드로 실패
- **AC-LOGIC-02**: 정순/역순 조합 규칙 및 채택 순서 재현
- **AC-MLOPS-01**: 데이터 스키마 위반 시 CI 파이프라인 실패
- **AC-MLOPS-02**: 배포 전 오프라인 기준선 미달 시 배포 차단
- **AC-MLOPS-03**: 운영 중 latency/품질 임계치 초과 시 알림 발생

---

## 8) TDD 실행 게이트
- **RED**: 트랙별 실패 테스트 먼저 작성
- **GREEN**: 최소 구현으로 테스트 통과
- **REFACTOR**: 외부 계약(입력/출력/오류/서빙스키마) 불변 유지

---

## 9) 성공 지표 (KPI)
- Domain 테스트 커버리지 `>=95%`
- 입력/출력/오류 계약 테스트 `100%`
- 추적성 매트릭스 전 행 테스트 연결 `100%`
- MLOps 파이프라인 게이트 통과율 `100%` (main 기준)
- 서빙 `p95 latency` 목표치 충족 (예: `<200ms`, 팀 기준값으로 확정)

---

## 10) Traceability 확장
기존 체인을 다음으로 확장:
- `Concept -> Rule -> UseCase -> Contract -> Test -> Component -> PipelineStage`

예:
- `INV-03(범위)` -> `UC-01` -> `Input schema` -> `T-UI-RED-03 / T-D-RED-04` -> `InputValidator` -> `Data Validation Job`

---

원하시면 다음 단계로, 제가 `docs/PRD_4x4_MagicSquare_TDD.md`를 이 구조에 맞춰 **실제 문서 형태로 직접 리라이팅**해드리겠습니다.

---

**User**

지금 정리한 컨셉으로 @docs/PRD_4x4_MagicSquare_TDD.md 파일을 분석해줘.

---

**Cursor**

지금 파일을 기준으로, 방금 합의한 `Dual-Track UI + Logic TDD with MLOps` 관점에서 **강점 / 누락 / 보완 우선순위**로 분석해드리겠습니다. 최신 내용 기준으로 다시 확인하고 정리할게요.

좋은 문서입니다. 현재 `docs/PRD_4x4_MagicSquare_TDD.md`는 **Dual-Track(UI/Logic) TDD PRD로는 완성도 높고**, `with MLOps` 관점에서는 **운영 트랙이 아직 비어 있는 상태**입니다.

## 분석 결과

- **Dual-Track 적합도**: 높음 (약 8.5/10)
- **MLOps 적합도**: 낮음 (약 3/10)
- **종합**: 현재 문서는 “Dual-Track TDD PRD”로는 매우 좋고, “Dual-Track + MLOps PRD”로 확장 필요

## 잘 되어 있는 부분

- `불변조건(Invariant)`이 명확해 테스트 전환이 쉽습니다.
- `Boundary Track`/`Domain Track` 분리가 선명합니다.
- 오류 코드 화이트리스트와 고정 메시지 원칙이 있어 계약 안정성이 좋습니다.
- `AC`, `TDD Gate`, `Traceability Matrix`가 있어 실행 가능한 문서 형태입니다.

## 지금 컨셉 대비 핵심 갭

- **Ops/MLOps Track 부재**
  - 현재 `6. Dual-Track 요구사항`에는 UI/Logic만 있고, 파이프라인/서빙/모니터링 계약이 없습니다.
- **성공 기준의 운영 지표 부재**
  - `4.2 측정 가능한 성공 기준`에 데이터 검증 실패율, 배포 게이트 통과율, latency/SLO 같은 운영 KPI가 없습니다.
- **MLOps 인수 기준(AC) 부재**
  - `8. 테스트 가능한 인수 기준`이 UI/Logic 중심이며, 데이터 스키마 깨짐/모델 성능 기준 미달/모니터링 알림 같은 AC가 없습니다.
- **추적성 체인 미확장**
  - 현재 매트릭스가 `... -> Component`에서 끝납니다.  
  - `with MLOps`라면 `... -> Pipeline Stage`까지 이어져야 합니다.
- **릴리스 승인 기준의 운영 게이트 부재**
  - 배포 전후 기준(오프라인 평가, 온라인 성능, 롤백 조건)이 없습니다.

## 문서 내부에서 조정이 필요한 표현

- `1. 문서 목적`의 “순수 로직 중심” 문구는 현재 구조에선 맞지만, **UI+Logic+MLOps 확장 문서**로 가려면 “순수 로직 중심”을 완화해 “계약 중심(로직+운영 포함)”으로 바꾸는 게 일관적입니다.
- `3.2 비범위`의 “네트워크/API 서버 구현”은 그대로 두되, “서빙 계약 정의(구현 아님)”는 범위로 분리하면 충돌이 줄어듭니다.

## 최소 수정으로 완성도 올리는 방법

- `6.3 MLOps Track` 신설: Data/Model/Serving/Monitoring 계약 정의
- `8`에 `AC-MLOPS-01~03` 추가
- `11` 매트릭스를 `Component -> PipelineStage`로 확장
- `12` 릴리스 기준에 배포 게이트(성능/품질/알림) 추가
- `4.2`에 운영 KPI 2~4개 추가

원하면 다음 답변에서 `docs/PRD_4x4_MagicSquare_TDD.md`에 바로 넣을 수 있는 **삽입용 문구(섹션별 문장 템플릿)**로 정확히 작성해드리겠습니다.

---

**User**

부족한 부분을 보완해서 @docs/PRD_4x4_MagicSquare_TDD.md  파일을 수정해줘.

---

**Cursor**

좋습니다. 기존 Dual-Track 구조는 유지하고, 문서 일관성을 깨지 않게 `MLOps Track` 요구사항·AC·추적성·릴리스 기준까지 연결되도록 바로 반영하겠습니다.

`docs/PRD_4x4_MagicSquare_TDD.md`를 요청하신 컨셉에 맞춰 보완했습니다.  
기존 Dual-Track 강점은 유지하고, **MLOps Track을 문서 계약 수준으로 추가**해 Tri-Track 형태로 정리했습니다.

주요 반영 내용:
- `6`장을 `Tri-Track 요구사항 (Dual-Track + MLOps Track)`으로 확장
- `6.3 MLOps Track` 신설
  - Data Contract
  - Model Artifact Contract
  - Serving Contract
  - Monitoring Contract
- 유스케이스에 `UC-06~08` 추가 (데이터 계약/서빙 계약/운영 알림)
- 인수기준에 `AC-05 MLOps 계약` 추가
- 추적성 매트릭스를 `Pipeline Stage`까지 확장
  - `Concept -> Rule -> Use Case -> Contract -> Test -> Component -> Pipeline Stage`
- 릴리스 승인 기준을 Tri-Track 기준으로 업데이트
- 목적/범위/성공지표에도 MLOps 관점(운영 게이트, 서빙 계약, 기준선 차단)을 반영

검증:
- 문서 수정 후 린트 진단 확인했고 문제 없습니다.

원하시면 다음으로, 이 PRD 기준에 맞는 **테스트 ID 네이밍 규약(`T-OPS-RED-*`)과 pytest 스켈레톤 파일 구조**까지 바로 만들어드릴게요.

---

**User**

지금까지 작업한 내용을 Report 폴더의 @Report/05_4x4-마방진-PRD-요구사항정의-보고서.md 파일에 업데이트해줘.

---

**Cursor**

요청하신 보고서 파일 구조를 먼저 확인한 다음, 방금 반영한 PRD 변경사항(Tri-Track/MLOps 확장)을 같은 형식으로 정확히 업데이트하겠습니다.

이제 보고서 파일은 PRD 원문 복사본 형태라, 요청하신 “작업 내용 업데이트 보고서” 형태로 전체를 정리해 덮어쓰겠습니다.

`Report/05_4x4-마방진-PRD-요구사항정의-보고서.md` 업데이트 완료했습니다.

반영한 내용:
- 기존 PRD 변경사항을 기준으로 **보고서 형식**으로 재작성
- Dual-Track 기반에서 **Tri-Track(Dual-Track + MLOps Track)** 확장 내용 정리
- 추가된 `UC-06~08`, `AC-05`, Traceability 확장(`Pipeline Stage`) 반영
- 릴리스 승인 기준의 운영 게이트 연결 조건 반영
- 현재 상태 평가, 기대 효과, 다음 권장 작업까지 포함

검증:
- 파일 저장 후 진단 확인했고 문제 없습니다.

원하시면 다음으로 `Report` 문서와 `docs/PRD_4x4_MagicSquare_TDD.md` 간 항목을 자동 대조하는 체크리스트 섹션도 추가해드릴게요.

