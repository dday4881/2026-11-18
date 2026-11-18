# 261118 B08 실행 결과 보고서

* **소속:** Cyberdyne Systems
* **보고서 번호:** Rpt No. 001
* **실습 내용:** 8번 `--mode fixture`, `--mode live` 실행 결과 보고서

제출 해야 하는 소요시간보단 꽤 오래 걸렸지만 샘플이 흥미로워 늦은 시간까지 매달려 완성한 결과 물입니다.

서버는 켜져있지만 설정이 오류로인해 연동이 되지않아 결과 값이 fixture와 live의 값이 일치하지 않는다는 것을 알았습니다.

성공 사례와 실패 사례라고 단정 지을 수 없지만, 어떠한 결과값이 나오던 생성된 output 폴더의 exercise_08.json 파일을 첨부하니 타 부서에서 이어 연구한다면
더 흥미로운 결과가 나올 것으로 보입니다.

---

## 실행 결과 값 (조건 : python main.py --mode fixture)

```json
{
  "exercise": 8,
  "level": 1,
  "source_mode": "simulated",
  "question": "서버는 어디에서 실행하나요?",
  "options": {
    "k": 3,
    "category": null
  },
  "retrieved": [
    {
      "id": 102,
      "title": "서버 실행",
      "content": "프로젝트 폴더에서 서버를 실행합니다.",
      "category": "development",
      "source_version": "knowledge_v1",
      "distance": 0
    },
    {
      "id": 106,
      "title": "데이터베이스 연결",
      "content": "PostgreSQL 접속 정보는 로컬 설정 파일에서 읽습니다.",
      "category": "development",
      "source_version": "knowledge_search_v2",
      "distance": 0
    },
    {
      "id": 107,
      "title": "패키지 설치",
      "content": "필요한 Python 패키지는 기존 가상환경에 추가합니다.",
      "category": "development",
      "source_version": "knowledge_search_v2",
      "distance": 0
    }
  ],
  "retrieved_count": 3,
  "human_evidence_ok": null,
  "next_step": "검토 후 Context 후보로 전달; LLM 답변 생성은 Day25 RAG에서 수행"
}
```
## 실행 결과 값 (조건 : python main.py --mode live)

```json
  File "C:\WorkSpace\20261118\mentee\01_basic\08_retriever_project\main.py", line 111, in <module>
    main()
  File "C:\WorkSpace\20261118\mentee\01_basic\08_retriever_project\main.py", line 104, in main
    result=run(args.mode,1,args)
  File "C:\WorkSpace\20261118\mentee\01_basic\08_retriever_project\main.py", line 84, in run
    hits=retrieve_candidates(question,mode,options['k'],options['category'],Path(__file__).with_name('.env'))
  File "C:\WorkSpace\20261118\mentee\01_basic\08_retriever_project\main.py", line 53, in retrieve_candidates
    check_data_ready(conn)
  File "C:\WorkSpace\20261118\mentee\common\day23kit\db.py", line 80, in check_data_ready
    if not exists:raise RuntimeError('실습 05 --mode live를 먼저 실행하여 검색 테이블과 문서 벡터를 저장하세요.')
RuntimeError: 실습 05 --mode live를 먼저 실행하여 검색 테이블과 문서 벡터를 저장하세요. """
```

## 재시도 후 오류 해결 완료

```json
{
  "exercise": 5,
  "level": 1,
  "source_mode": "pgvector_exact",
  "table": "day23_search_docs",
  "model": "intfloat/multilingual-e5-small",
  "prepared_count": 9,
  "first_passage": "passage: 실습 파일 보관 실습 파일은 개인 폴더에 보관합니다.",
  "sql_schema": "CREATE TABLE IF NOT EXISTS day23_search_docs (\n    id integer PRIMARY KEY,\n    title text NOT NULL,\n    content text NOT NULL,\n    category text NOT NULL,\n    source_version text NOT NULL,\n    embedding_model text NOT NULL,\n    embedding vector(384) NOT NULL\n)",
  "sql_topk": "SELECT id,title,content,category,source_version,\n     embedding_model,embedding <=> %s AS distance\nFROM day23_search_docs WHERE embedding_model=%s\nORDER BY embedding <=> %s ASC LIMIT %s",
  "hits": [
    {
      "id": 102,
      "content": "프로젝트 폴더에서 서버를 실행합니다.",
      "distance": 0.114599
    },
    {
      "id": 103,
      "content": "오류 메시지와 시도한 작업을 함께 적습니다.",
      "distance": 0.195967
    },
    {
      "id": 107,
      "content": "필요한 Python 패키지는 기존 가상환경에 추가합니다.",
      "distance": 0.19779
    }
  ]
}