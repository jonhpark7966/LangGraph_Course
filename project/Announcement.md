
### 코드 설명
- evaluate.py: 채점 코드
- fastapi_langchain_start.py: 랭체인 기반 시작 코드
- fastapi_langgraph_start.py: 랭그래프 기반 시작 코드

```bash
# 환경 셋업
source 3kingdoms_proj_venv/bin/activate

# (추천) .env 에 API_KEY 셋업
source .env

# LLM 어플리케이션 배포
./fast_..._start.py

# 평가 수행
./evaluate.py
```

## 목표
- 삼국지 퀴즈를 잘 맞추는 LLM Application 을 만들자


## 제약
- 비용
	- 배부된 API_KEY 사용, $40 제한, 로컬 모델은 마음 껏 사용 가능
- 데이터
	- train/test 데이터 셋 오라클 금지
- 시간
	- evaluate 에서 평균 10초
	- p50, p99 는 무관


## 참고
- 테스트 데이터 비공개
- LLM as judge (Qwen2.5-7B-Instruct) 로 local gpu 에서 평가
	- 평가 프롬프트는 evaluate.py 참조
