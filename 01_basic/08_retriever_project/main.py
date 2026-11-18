"""Day23 실습 08 · AI Agent용 Retriever (기본필수, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""

# [모듈 임포트 영역] 실행에 필요한 표준 라이브러리와 실습용 보조 도구를 불러옵니다.
import argparse  # 터미널 명령줄 인자(--mode, --question 등)를 파싱하기 위한 모듈
import sys       # 파이썬 시스템 경로(sys.path)를 제어하기 위한 모듈
from pathlib import Path  # 파일 및 폴더 경로를 객체로 안전하게 다루기 위한 모듈

# 현재 파일 위치에서 두 단계 상위 폴더의 'common' 디렉터리를 모듈 검색 경로에 추가합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'common'))

from time import perf_counter  # 검색 소요 시간을 밀리초 단위로 정밀 측정하기 위한 타이머
from day23kit.fixtures import fixture_search  # 오프라인 시연용 모의 검색 함수
from day23kit.embedding import get_encoder, encode_question  # E5 임베딩 모델 로드 및 질문 벡터화 함수
from day23kit.db import connect_db, exact_topk, check_data_ready  # PostgreSQL DB 연결, 데이터 확인, 유사도 검색 함수
from day23kit.io import save_result  # 최종 실행 결과를 JSON 파일로 저장하는 함수


# BEGIN D23-08-B01 (자동 채점기 및 실습 구역 표시용 시작 주석)
def validate_question(question):
    """
    TODO D23-08-B01 · validate_question
        질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
        빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
        API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.
    """  # Where is John Conner (작성자가 남긴 영화 터미네이터 패러디 메모 주석)

    # [기존 주석 코드 설명] 초기 시도했던 코드로, 함수 내부에서 자기 자신을 재귀 호출하고 존재하지 않는 args를 참조해 무한 루프/에러를 유발하므로 주석 처리하여 비활성화한 줄입니다.
    # question=validate_question(getattr(args,'question','존 코너는 어디에 있나요?'))

    # 1. 입력값이 문자열(str) 타입이 아니면 ValueError 예외를 발생시켜 차단합니다.
    if not isinstance(question, str):
        raise ValueError

    # 2. 문자열 앞뒤의 불필요한 공백과 줄바꿈을 제거합니다.
    cleaned = question.strip()

    # 3. 공백을 지운 결과가 빈 문자열이라면 유효한 질문이 아니므로 ValueError를 발생시킵니다.
    if cleaned == "":
        raise ValueError

    # [기존 주석 코드 설명] 실습 시작 전 "아직 구현되지 않음"을 알리던 기본 템플릿 예외 코드입니다. 구현을 마쳤으므로 주석 처리해 비활성화했습니다.
    # TODO D23-08-B01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    # raise NotImplementedError("D23-08-B01: 직접 구현하세요")

    # 4. 검증과 정리가 끝난 깨끗한 질문 문자열을 반환합니다.
    return cleaned
# END D23-08-B01 (자동 채점기 및 실습 구역 표시용 종료 주석)


# BEGIN D23-08-B02
def retrieve_candidates(question, mode, k, category, env_file):
    """
    TODO D23-08-B02 · retrieve_candidates
        fixture면 교육용 fixture_search, live면 E5 query Embedding → pgvector Exact SQL을 사용하세요.
        실제 live는 exercise05에서 9개 자료를 먼저 저장해야 합니다.
        DB 연결 실패를 빈 결과 []로 바꾸지 말고 예외를 전달하세요.
    """
    # [기존 주석 코드 설명] 미구현 상태를 알리던 초기 템플릿 주석 및 예외 코드입니다.
    # TODO D23-08-B02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    # raise NotImplementedError("D23-08-B02: 직접 구현하세요")

    # 1. fixture 모드일 경우: DB나 AI 모델 없이 내장된 모의 데이터에서 상위 k개 후보를 검색해 반환합니다.
    if mode == "fixture":
        return fixture_search(question, k=k, category=category)

    # 2. live 모드일 경우: 실제 PostgreSQL(pgvector)과 E5 모델을 연결해 검색합니다.
    elif mode == "live":
        # .env 설정 파일을 읽어 데이터베이스에 연결합니다. (실패 시 예외가 그대로 상위로 전달됨)
        conn = connect_db(env_file)
        try:
            check_data_ready(conn)  # DB 테이블에 실습용 문서 데이터가 정상적으로 적재되어 있는지 확인합니다.
            encoder = get_encoder()  # E5 임베딩 인코더 모델을 불러옵니다.
            q_vec = encode_question(encoder, question)  # 사용자 질문을 숫자 배열(임베딩 벡터)로 변환합니다.
            return exact_topk(conn, q_vec, k, category)  # 질문 벡터와 가장 가까운 상위 k개 문서를 DB에서 찾아 반환합니다.
        finally:
            conn.close()  # 검색이 성공하든 중간에 에러가 나든 DB 연결을 반드시 안전하게 닫습니다.
# END D23-08-B02


# BEGIN D23-08-B03
def format_candidates(hits):
    """
    TODO D23-08-B03 · format_candidates
        후보의 id/title/content/category/source_version/distance를 반환하세요.
        검색된 원문을 요약·변조하지 않고, distance는 숫자 그대로 둡니다.
        답변 상태(answered)를 자동으로 부여하지 마세요.
    """
    # [기존 주석 코드 설명] 미구현 상태를 알리던 초기 템플릿 주석 및 예외 코드입니다.
    # TODO D23-08-B03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    # raise NotImplementedError("D23-08-B03: 직접 구현하세요")

    # 검색된 각 문서(h)에서 필요한 6가지 핵심 필드만 추출하여 새로운 딕셔너리 리스트로 규격화합니다.
    # 원문(content)과 유사도 거리(distance)는 변형하지 않고 원본 값 그대로 유지합니다.
    return [{'id': h['id'], 'title': h['title'], 'content': h['content'],
             'category': h['category'], 'source_version': h['source_version'],
             'distance': (h['distance'])} for h in hits]
# END D23-08-B03


# [전체 파이프라인 실행 함수] 검증 -> 검색 -> 포맷팅 -> 결과 패키징 과정을 하나로 묶어 실행합니다.
def run(mode, level, args):
    # 입력받은 질문을 validate_question으로 검증합니다.
    question = validate_question(getattr(args, 'question', '서버는 어디에서 실행하나요?'))
    # level 1(기본 단계)이면 k=3, category=None으로 고정하고, 그 이상이면 사용자 입력값을 사용합니다.
    k = 3 if level == 1 else args.k
    category = None if level == 1 else args.category
    if level >= 2:
        options = validate_options(k, category)
    else:
        options = {'k': k, 'category': category}

    # 검색 시작 시각을 기록한 뒤 retrieve_candidates로 후보 문서를 검색합니다.
    t0 = perf_counter()
    hits = retrieve_candidates(question, mode, options['k'], options['category'], Path(__file__).with_name('.env'))
    # 검색에 걸린 총 시간을 밀리초(ms) 단위로 계산합니다.
    elapsed = (perf_counter() - t0) * 1000

    # 검색 결과를 표준 출력 형식에 맞게 정제합니다.
    formatted = format_candidates(hits)

    # 최종 결과 딕셔너리를 구성합니다. (실제 LLM 답변 생성 전 단계이므로 human_evidence_ok는 None으로 둡니다.)
    result = dict(
        exercise=8,
        level=level,
        source_mode='simulated' if mode == 'fixture' else 'pgvector_exact',
        question=question,
        options=options,
        retrieved=formatted,
        retrieved_count=len(formatted),
        human_evidence_ok=None,
        next_step='검토 후 Context 후보로 전달; LLM 답변 생성은 Day25 RAG에서 수행'
    )
    # 심화 단계(level 2, 3)일 경우 실행 리포트 및 모델 버전 검증 결과를 추가로 담습니다.
    if level >= 2:
        result['run_report'] = make_run_report(question, hits, mode, elapsed)
    if level >= 3:
        result['contract_check'] = check_model_and_versions(hits, mode)
    return result


# [프로그램 진입점] 터미널 명령줄 인자를 해석해 실행하고 결과를 파일로 저장·출력합니다.
def main():
    parser = argparse.ArgumentParser(description='Day23 실습 08 · AI Agent용 Retriever')
    parser.add_argument('--mode', choices=['fixture', 'live'], default='fixture',
                        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    parser.add_argument('--question', default='서버는 어디에서 실행하나요?', help='검색 질문')
    parser.add_argument('--k', type=int, default=3, help='반환할 최대 검색 후보 (1~9)')
    parser.add_argument('--category', default=None, choices=['course', 'development', 'support'], help='Metadata 분류 필터')
    args = parser.parse_args()

    # level 1 기준으로 검색 파이프라인을 실행합니다.
    result = run(args.mode, 1, args)
    # 결과를 현재 폴더의 'exercise_08.json' 파일로 저장합니다.
    path = save_result(Path(__file__).resolve().parent, 'exercise_08.json', result)

    # 저장된 결과를 터미널 화면에도 읽기 좋은 JSON 형식으로 출력합니다.
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print('결과 저장:', path)


# 이 파일이 다른 모듈에 임포트되지 않고 직접 실행될 때만 main() 함수를 호출합니다.
if __name__ == '__main__':
    main()

""" 출력 결과 값 실행 코드 : python main.py --mode fixture
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
  "next_step": "검토 후 Context 후보로 전달; LLM 답변 생성은 Day25 RAG에서 수행" """


""" 출력 결과 값 실행 코드 : python main.py --mode live
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

