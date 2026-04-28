# 09. MagicSquare 테스트/커버리지 실행 보고서

## 1) 보고서 개요

- 프로젝트: `MagicSquare_11`
- 보고 일시: 2026-04-28
- 보고 범위: 현재 워킹트리 기준 테스트 실행 결과, 커버리지 측정 결과, RED 복구 커밋 내역
- 기준 명령:
  - `pytest -q`
  - `pytest --cov=control --cov=entity --cov=boundary --cov-report=term-missing`

---

## 2) 실행 환경

- OS: Windows 10
- Shell: PowerShell
- Python: 3.10.11
- Pytest: 9.0.3
- Plugin: `pytest-cov 7.1.0`

---

## 3) 테스트 실행 결과 요약

### 3.1 전체 테스트

- 실행 명령: `pytest -q`
- 결과: **27 PASS / 0 FAIL**

### 3.2 RED 테스트 복구 결과

- 대상 파일: `tests/red/test_red_phase_cases.py`
- 결과: **13 PASS / 0 FAIL**
- 복구 완료 항목:
  - 보드 크기 검증 (`E_MATRIX_SIZE`)
  - 값 범위 검증 (`0 or 1..16`)
  - 0 제외 중복 금지
  - 빈칸 개수 정확히 2개
  - 누락 숫자 정렬 탐색
  - 조합 해석(정방향 우선, 역방향 fallback, 실패 시 `E_NO_VALID_COMBINATION`)
  - 오류 코드 whitelist 매핑
  - 출력 `int[6]` 스키마 정규화
  - 마방진 판정 규칙

---

## 4) 커버리지 측정 결과

- 실행 명령:
  - `pytest --cov=control --cov=entity --cov=boundary --cov-report=term-missing`
- 결과: **TOTAL 91%** (`115` statements, `10` missed)

### 4.1 미커버 파일(주요)

- `boundary/api/request_validator.py` : `0%` (라인 `3-10`)
- `control/use_cases/solve_magic_square.py` : `0%` (라인 `3-8`)
- `entity/models/board.py` : `82%` (라인 `14`, `21`)

### 4.2 참고

- 현재 기준 기능 테스트는 모두 통과(`27 passed`)했으며, 잔여 커버리지 갭은 미연결 Boundary/API 계층에 집중됨
- 커버리지는 실행된 라인 비율이며, 계약 준수 여부는 테스트 결과와 함께 해석해야 함

---

## 5) 산출물

- 커버리지 DB: `.coverage`
- HTML 리포트: `htmlcov/index.html`
- 본 보고서: `Report/09_MagicSquare_테스트_커버리지_실행보고서.md`

### 5.1 이번 복구 작업 커밋

- `2be7afd` `feat: validate board matrix size at creation`
- `942e376` `feat: enforce domain value range rule`
- `64076bb` `feat: enforce nonzero uniqueness rule`
- `cb46662` `feat: validate exact blank count in boundary input`
- `54f252f` `feat: compute sorted missing numbers from matrix`
- `39c2fd9` `feat: resolve blank combinations using magic-sum validation`
- `c295ef7` `feat: restrict boundary error codes to whitelist`
- `19e9967` `feat: normalize boundary solution output to int6`

---

## 6) 다음 액션 제안

1. `boundary/api/request_validator.py`, `control/use_cases/solve_magic_square.py`에 대한 실행 경로 테스트 추가
2. `board.py` 생성/정상 시나리오 테스트를 보강해 Entity 모델 커버리지 90%+ 확보
3. 필요 시 `pytest --cov=. --cov-branch --cov-report=html`로 분기 커버리지 점검
4. PR 생성 전 `pytest -q && pytest --cov=control --cov=entity --cov=boundary --cov-report=term-missing` 재검증

