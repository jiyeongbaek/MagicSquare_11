# 09. MagicSquare 테스트/커버리지 실행 보고서

## 1) 보고서 개요

- 프로젝트: `MagicSquare_11`
- 보고 일시: 2026-04-28
- 보고 범위: 현재 워킹트리 기준 테스트 실행 결과 및 커버리지 측정 결과
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
- 결과: **27개 중 16 PASS / 11 FAIL**

### 3.2 주요 실패 영역

- `tests/red/test_red_phase_cases.py` 중심으로 실패 발생
- 실패 유형 요약:
  - 보드 크기 검증 미동작 (`E_MATRIX_SIZE`)
  - 값 범위 검증/중복 검증 미동작
  - 빈칸 개수 검증 미동작
  - 누락 숫자 탐색 미동작
  - 조합 해석(resolve) 미동작
  - 오류 코드 화이트리스트 매핑 미동작
  - 출력 `int[6]` 포맷 매핑 미동작
  - 마방진 판정 규칙 미동작

---

## 4) 커버리지 측정 결과

- 실행 명령:
  - `pytest --cov=control --cov=entity --cov=boundary --cov-report=term-missing`
- 결과: **TOTAL 86%** (`59` statements, `8` missed)

### 4.1 미커버 파일(주요)

- `boundary/api/request_validator.py` : `0%` (라인 `3-10`)
- `control/use_cases/solve_magic_square.py` : `0%` (라인 `3-8`)

### 4.2 참고

- 일부 파일은 커버리지가 높게 표시되어도, RED 테스트 실패로 기능 완성 상태로 보기는 어려움
- 커버리지는 실행된 라인 비율이며, 도메인 규칙의 기대 동작 충족 여부는 실패 테스트 결과를 우선 판단해야 함

---

## 5) 산출물

- 커버리지 DB: `.coverage`
- HTML 리포트: `htmlcov/index.html`
- 본 보고서: `Report/09_MagicSquare_테스트_커버리지_실행보고서.md`

---

## 6) 다음 액션 제안

1. `tests/red/test_red_phase_cases.py` 실패 11건을 우선 GREEN 구현으로 복구
2. 복구 후 `pytest -q` 재실행하여 `27 passed` 상태 확인
3. 동일 커맨드로 커버리지 재측정 후 목표치(예: Domain 95% 이상) 대비 갭 점검
4. 필요 시 `pytest --cov=. --cov-branch --cov-report=html`로 분기 커버리지 보강

