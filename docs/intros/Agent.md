# Agentic Application

**에이전트 (Agent)** 는 LLM (또는 LMM, FM) 을 잘 사용하는 가장 대표적인 방법입니다. 글을 작성하고 있는 현시점 기준의 (24.09) ChatGPT 서비스도 하나의 Agent 라고 볼 수 있습니다. 사용자와 대화를 하면서 필요에 따라 웹브라우징도 하고, 코드를 작성해서 수행해보기도 하고, dalle 를 통해 그림을 그려주기도 하죠. GPT 라는 LLM 에 Agent 개념이 추가되어 ChatGPT라는 보다 똑똑한 서비스를 만든 것입니다.  

LangGraph 에서는 이를 Agent 라고 칭하기 보다는 "Agentic" 한 시스템이다 라고 표현합니다. 명확한 Agent 라는 기준은 없고, LLM 에 Agentic 한 동작들을 추가한 시스템 들이 있는 것이죠.  

Agentic 한 시스템은 LLM 이 직접 행동을 판단하고 수행하는 것을 의미합니다. 대표적으로는 아래와 같은 예시가 있겠네요.
- LLM 을 이용한 라우팅 
- LLM 이 직접 어떤 도구를 사용할지 결정
- 생성된 답변이 충분한지 아닌지 LLM 이 다시 판단
  
예를 들자면, 사용자가 "지구 표면적 구해봐" 라고 했을 때, LLM 이 "xxx 이다" 라고 대답했다고 가정해보겠습니다. 이 답변을 LLM 이 다시 읽어보고 틀렸는지 판단하고, 웹브라우징을 할지, 어떤 데이터베이스를 찾아볼기 결정하고, 다시 올바른 답변을 하는 헹위가 모두 Agentic한 동작입니다.  

위 행위들이 loop 을 돌면서 동작한다면, 더욱 Agentic 하다고 볼 수 있습니다.  

LangGraph 에서 정의한 Agentic 한 동작들은 다음과 같습니다.  

- [Tool calling](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/#tool-calling): 무엇이든 (ex. 웹브라우징, API 호출) 다른 행위를 하고 옵니다.
- [Memory](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/#memory): 대화 내용이나 앞선 동작들의 맥락 정보들을 기억합니다.
- [Planning](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/#planning): LLM 이 어떤 동작을 할지 계획합니다, 이것도 LLM 이 생성합니다.

# LangGraph 의 특징

LangGraph는 Agentic 시스템을 사용자들이 쉽게 만들 수 있도록 LangChain 에서 만든 프레임워크입니다.  

---
필자의 의견을 첨언하자면,
- LangChain이 애초에 LLM application 을 잘 만들기 위한 프레임워크이고, 당연히 Agent 구현을 지원했습니다.
- 그런데 LangChain 의 AgentExecuter 는 제약이 많이 있어서 product level 에서 사용하기가 어려웠습니다. 특히 중간 개입이 안되어 초기 구현은 매우 쉬웠으나, 디테일한 컨트롤이 불가했죠.
- 애초에 LangChain이 GPT3 출시와 ChatGPT 출시 사이에 나온 도구이고, 사용자들의 진입장벽을 낮춰주는 도구임을 감안하면 이해가 되는 영역입니다.
- 사용자들은 좋은 Agentic 시스템을 만들기 위해 LangChain 을 이탈했고, 이를 보완하기 위해 출시한 프레임워크가 LangGraph 입니다.
- [LangChain을 더 이상 쓰지 않는 이유 - 해커뉴스 쓰레드](https://news.ycombinator.com/item?id=40739982) 를 참조하시면, 다른 사용자들의 의견과 LangChain 의 창업자인 Harrison의 생각/방향성 을 보실 수 있습니다. 직접 harrison이 댓글로 해명(?) 하는 내용을 보실 수 있습니다. 
---

LangGraph에서 주장하는 본인들의 장점 (Agentic 시스템을 만들기 위한 특장점) 은 다음과 같습니다.

- [Controllability](https://langchain-ai.github.io/langgraph/how-tos/#controllability)
- [Human-in-the-Loop](https://langchain-ai.github.io/langgraph/how-tos/#human-in-the-loop)
- [Streaming First](https://langchain-ai.github.io/langgraph/how-tos/#streaming)


## Controllabillty

앞서 뽑은 LangChain 의 부족한 점이 디테일한 컨트롤이 보완되어 왔습니다.  
High-Level API를 지원하는 LangChain과 다르게, LangGraph는 **"Extremely Low Level"** 이라고 표현합니다. 그래서 사용자 (개발자) 는 아주 자세하게 컨트롤이 가능하고 reliable 한 시스템을 개발할 수 있죠. 

## Human-in-the-loop

