# 10. MagicSquare 리팩토링 사전분석 보고서

## 1) 보고서 개요

- 프로젝트: `MagicSquare_11`
- 보고 일시: 2026-04-28
- 목적: 리팩토링 착수 전, 코드 수정 없이 현재 상태를 구조/품질 관점에서 점검
- 분석 범위:
  - 테스트 파일 존재 여부 확인
  - 코드 스멜 점검
  - ECB(Entity-Control-Boundary) 역할 적합성 점검
  - SRP(단일 책임 원칙) 위반 후보 점검
  - 리팩토링 우선순위 및 검증 계획 수립

---

## 2) 사전 확인 결과

### 2.1 테스트 파일 존재 여부

- `test_*.py` 파일 존재 확인
  - `tests/test_tc_spec_executable.py`
  - `tests/red/test_red_phase_cases.py`

### 2.2 테스트 없이 리팩토링을 시작하면 안 되는 이유

- 테스트가 없으면 기존 동작이 깨져도 즉시 감지할 안전망이 없어 회귀 버그 위험이 커진다.

---

## 3) 코드 스멜 분석 결과(초기 점검)

| 파일명 | 줄번호 | 스멜 종류 | 문제 설명 | 우선순위 |
|---|---:|---|---|---|
| `tests/test_tc_spec_executable.py` | `25-105` | 중복 코드 | 운영 코드와 유사한 검증/판정/조합 로직을 테스트 파일에서 재구현하여 변경 동기화 비용과 불일치 위험이 큼 | 높음 |
| `tests/red/test_red_phase_cases.py` | `58-64`, `91-97`, `101-106`, `133-138` | 중복 코드 | 유사한 4x4 매트릭스 리터럴이 반복되어 수정 시 다중 편집 필요 | 중간 |
| `magicsquare/gui/app.py` | `35-61` | 긴 함수 | `_build_ui`가 위젯 생성/설정/레이아웃 조립을 한 번에 수행 | 중간 |
| `tests/test_tc_spec_executable.py` | `25-47` | 긴 함수 | `validate_matrix`가 크기/빈칸/범위/중복 검증을 동시에 수행 | 중간 |
| `tests/test_tc_spec_executable.py` | `34`, `42`, `63`, `70-72`, `110-114`, `213-216` | 매직 넘버 | `4`, `16`, `17`, `34` 리터럴 반복 사용으로 변경 대응성 저하 | 중간 |
| `control/use_cases/solve_magic_square.py` | `6-8` | 사용하지 않는 함수(스텁) | 고정값 반환 스텁이 실제 흐름과 분리되어 유지보수 혼선 유발 | 높음 |
| `boundary/api/request_validator.py` | `6-10` | 사용하지 않는 함수 | 현재 사용 경로가 없고 검증 범위가 제한적 | 중간 |
| `control/services/combination_resolver.py` | `34-35` | 이해하기 힘든 이름 | `rn1`, `rn2` 이름이 의미 전달력이 낮음 | 낮음 |

> 참고: 위 표는 초기 스멜 점검 결과이며, 사용자 요청에 따라 일부 항목은 테스트 파일 포함으로 식별됨.

---

## 4) ECB(Entity-Control-Boundary) 관점 분석

> 본 섹션은 테스트 코드를 제외한 운영 코드 기준으로 점검함.

### 4.1 역할 진단 요약

- `entity/models/board.py`
  - 의도: Entity(데이터)
  - 현황: 데이터 보관 책임 + 검증 책임이 혼재
- `entity/rules/*.py`
  - 의도/현황: Entity 규칙 역할 대체로 적합
  - 주의: 일부 파일이 Control 상수 의존
- `control/services/*.py`
  - 의도/현황: Control 비즈니스 로직 역할 대체로 적합
- `control/use_cases/solve_magic_square.py`
  - 의도: Control 유스케이스
  - 현황: 스텁(고정값 반환) 상태
- `boundary/api/*.py`
  - 의도/현황: Boundary 역할 대체로 적합
  - 주의: `request_validator`는 경계 검증 강도 부족
- `magicsquare/gui/app.py`
  - 의도/현황: UI 경계 역할 중심
  - 점검 결과: UI가 직접 마방진 계산/판정하는 코드 미확인

### 4.2 위치 조정 권장

- `control/constants/matrix.py`
  - 권장 이동: `entity/constants/` 또는 `core/constants/`
- `control/constants/error_codes.py`
  - 권장 이동: `boundary/api/` 또는 `contracts/`
- `magicsquare/domain.py`
  - 권장: 도메인 상수 소유권을 Entity/Core로 명확화
- `magicsquare/boundary.py`
  - 권장: 서비스 직접 호출 대신 UseCase 경유 구조로 정리

### 4.3 Entity/Control 혼재 지점

- `entity/models/board.py`: 데이터 보관 + 검증 혼재
- `entity/rules/value_range_rule.py`: Entity 규칙이 Control 상수 의존
- `magicsquare/domain.py`: 도메인 성격 모듈이 Control 상수 의존

---

## 5) SRP(단일 책임 원칙) 위반 후보

- `entity/models/board.py:17`
  - `Board.from_matrix()`가 객체 생성과 입력 검증을 동시에 수행
- `control/services/combination_resolver.py:22`
  - 조합 판정 로직과 결과 포맷 조립을 동시에 수행
- `boundary/api/response_mapper.py:13`
  - 응답 매핑과 좌표 보정(clamp) 규칙 적용을 동시에 수행
- `magicsquare/gui/app.py`
  - UI 외 직접 비즈니스 계산(`if total == 34`) 패턴은 미확인

---

## 6) 리팩토링 대상 목록(우선순위 순)

| 순번 | 대상 파일 | 문제 | 적용 기법 | 우선순위 |
|---:|---|---|---|---|
| 1 | `entity/models/board.py` | 데이터 + 검증 책임 혼재 | Extract Method + Move Responsibility | 높음 |
| 2 | `control/services/combination_resolver.py` | 판정 + 포맷 조립 책임 혼재 | Extract Function | 높음 |
| 3 | `boundary/api/response_mapper.py` | 매핑 + 정책 적용 혼재 | Separate Query from Transformation | 중간 |
| 4 | `control/use_cases/solve_magic_square.py` | 유스케이스 스텁 상태 | Introduce Orchestration | 중간 |
| 5 | `magicsquare/boundary.py` | 서비스 직접 호출 | Redirect Through UseCase | 중간 |
| 6 | `magicsquare/domain.py`, `control/constants/matrix.py` | 상수 소유 계층 모호 | Move Constants Module | 중간 |
| 7 | `boundary/api/request_validator.py` | 경계 검증 강도 부족 | Strengthen Contract Validation | 낮음 |
| 8 | `magicsquare/gui/app.py` | UI 구성 함수 과대 | Extract Method | 낮음 |

---

## 7) 테스트 선행 필요 항목

- `entity/models/board.py`의 `Board.from_matrix()`
- `control/services/combination_resolver.py`의 `resolve_combination()`
- `boundary/api/response_mapper.py`의 `map_solution_to_int6()`
- `magicsquare/boundary.py`의 `validate()`, `solve()`
- `control/use_cases/solve_magic_square.py`의 `solve_magic_square()`
- `boundary/api/request_validator.py`의 `validate_request()`

---

## 8) 리팩토링 후 검증 방법

### 8.1 회귀 테스트 실행 명령어

- `pytest -q`
- `pytest --cov=. --cov-report=term-missing`
- `pytest -q tests/red/test_red_phase_cases.py tests/test_tc_spec_executable.py`

### 8.2 외부 동작(기능) 동일성 확인

- 대표 입력셋(정상/역순 fallback/실패)에 대한 결과 `int[6]` 및 에러코드를 리팩토링 전후 비교
- Boundary 진입점 기준 반환 타입/길이/좌표 범위(1~4) 동일성 확인
- UI 수동 스모크로 성공/오류 메시지 흐름 동일성 확인

---

## 9) 결론

- 현재 코드베이스는 기본 동작 구현은 진행되었으나, 계층 책임 분리(ECB)와 단일 책임(SRP) 측면에서 구조 개선 여지가 명확함.
- 리팩토링은 테스트 안전망을 전제로, `Entity 책임 정리 -> Control 오케스트레이션 정리 -> Boundary 계약 명확화` 순으로 진행하는 것이 리스크가 가장 낮음.
