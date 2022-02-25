# 29-2nd-needed-backend

## Introduction
> 👉 I need YOU for the world’s leading companies!

1. 다양한 일자리를 카테고리별로 나눠 구직자에게 접근성이 용이하게 합니다.
2. 잡포스팅 외에도 다양한 이벤트, 직군별 연봉정보 등을 제공합니다.
3. 각종 테마에 대하여 서로 의견을 주고받을 수 있는 커리어 커뮤니티를 가지고 있습니다.

[Wanted](https://www.wanted.co.kr/)의 클론 코딩 프로젝트입니다.


## 개발 인원 및 기간
- 기간 : 21.02.14 ~ 22.02.25
- Frontend 4명 : 곽승현, 박무선, 윤남주, 장예지
- Backend  2명 : 김준영, 김성수

[Frontend Git Repository](https://github.com/wecode-bootcamp-korea/29-2nd-needed-frontend)

## 적용 기술 및 구현 기능
- `Frontend`       : JavaScript, React.js, SASS, React-router-dom, Styled Component
- `Backend`        : Python, Django, MySQL, AWS(EC2, RDS, S3), Docker
- `협업 및 일정 관리` : Git, Github, Slack, Trello, Notion, Figma

## Backend Features

#### Part
|               | 구현 파트                        |
| :-----------: | :------------------------------- |
| <b>김준영</b> | 모델링, 소셜로그인, 채용리스트, 회사/채용 상세정보, 직군별 연봉, 월간 구독 서비스 Needed+    |
| <b>김성수</b> | 모델링, 직업 카테고리 리스트, 이력서(파일) 업로드 및 삭제/조회(soft-delete 적용) ,검색 기능  |

#### User API
- 회원가입/로그인 - 소셜 로그인(OAuth 2.0), KakaoAPI 모듈화(토큰, 사용자 정보 가져오기)
- 마이페이지 정보수정 - 개인정보 수정 기능
- 직군별 연봉 - 사용자가 입력한 연봉/경력(연차)를 토대로 직군/연차별 연봉 데이터 전송

#### Recruitment API
- 직군(카테고리), 직무(서브카테고리)
- 키워드를 통한 채용 리스트 정렬(filtering, sorting) - 직군,직무,지역 채용보상금, 날짜순
- 채용 상세 페이지(채용 회사, 위치, 채용보상금 등등)
- 검색 기능

#### Company API
- 회사 상세 페이지(모집하는 채용, 태그, 회사정보 등등)
- 검색 기능

#### Application API
- 채용 지원(soft-delete)
- 회사별 지원 내역

#### Resume API
- 이력서 파일 업로드, 딜리트(aws s3 모듈화)
- 유저가 업로드한 이력서 내역

#### Neededplus API
- 월간 아티클 구독 서비스 Needed+ - 회원의 구독 여부를 받아서(GET) 구독시 구독 여부 값과 구독 날짜를 DB에 전송(PATCH)

## Reference
[API Documentation](https://grey-zipper-891.notion.site/Backend-a4789355b74e4b29bc1a5b6eafd913b2)

[db.diagram](https://dbdiagram.io/d/6209d6bd85022f4ee589334b)
