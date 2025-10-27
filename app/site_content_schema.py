"""
Central definition of editable site content.

This module lists every text fragment that should be editable from the
administrator console.  Each item contains metadata that the management UI
uses to render a friendly editor and to seed default values in the database.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class ContentField:
    key: str
    label: str
    default: str
    input_type: str = "textarea"  # either "text" or "textarea"
    format: str = "plain"  # either "plain" or "markdown"
    help_text: Optional[str] = None


@dataclass(frozen=True)
class ContentSection:
    id: str
    title: str
    description: str
    fields: List[ContentField]


SECTION_DEFINITIONS: List[ContentSection] = [
    ContentSection(
        id="navigation",
        title="상단 메뉴",
        description="홈페이지 상단 네비게이션 바에 노출되는 문구들입니다.",
        fields=[
            ContentField(
                key="nav_brand_title",
                label="로고 옆 교회 이름",
                default="University Church",
                input_type="text",
            ),
            ContentField(
                key="nav_home_label",
                label="메뉴 - Home",
                default="Home",
                input_type="text",
            ),
            ContentField(
                key="nav_about_label",
                label="메뉴 - 교회 소개",
                default="교회 소개",
                input_type="text",
            ),
            ContentField(
                key="nav_intro_label",
                label="메뉴 - 기독교 소개",
                default="기독교 소개",
                input_type="text",
            ),
            ContentField(
                key="nav_sermons_label",
                label="메뉴 - 설교",
                default="설교",
                input_type="text",
            ),
            ContentField(
                key="nav_bible_study_label",
                label="메뉴 - 성경 공부",
                default="성경 공부",
                input_type="text",
            ),
            ContentField(
                key="nav_church_life_label",
                label="메뉴 - 교회 생활",
                default="교회 생활",
                input_type="text",
            ),
            ContentField(
                key="nav_resources_label",
                label="메뉴 - 자료공유",
                default="자료공유",
                input_type="text",
            ),
            ContentField(
                key="nav_messages_label",
                label="메뉴 - 받은 메시지 (목사님만 표시)",
                default="받은 메시지",
                input_type="text",
            ),
            ContentField(
                key="nav_login_label",
                label="메뉴 - 관리자 로그인",
                default="관리자 로그인",
                input_type="text",
            ),
            ContentField(
                key="nav_logout_label",
                label="메뉴 - 로그아웃",
                default="Logout",
                input_type="text",
            ),
            ContentField(
                key="nav_english_label",
                label="우측 버튼 - 영어 보기",
                default="ENGLISH",
                input_type="text",
            ),
            ContentField(
                key="nav_youtube_label",
                label="우측 버튼 - 유튜브",
                default="UChurchMD TV",
                input_type="text",
            ),
            ContentField(
                key="nav_legacy_label",
                label="우측 버튼 - 이전 홈페이지",
                default="이전 홈페이지",
                input_type="text",
            ),
            ContentField(
                key="nav_manage_content_label",
                label="메뉴 - 콘텐츠 관리 (목사님만 표시)",
                default="콘텐츠 관리",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="login",
        title="관리자 로그인 페이지",
        description="관리자 로그인 화면에 표시되는 문구입니다.",
        fields=[
            ContentField(
                key="login_page_title",
                label="브라우저 탭 제목",
                default="관리자 로그인",
                input_type="text",
            ),
            ContentField(
                key="login_heading",
                label="페이지 상단 제목",
                default="관리자 로그인",
                input_type="text",
            ),
            ContentField(
                key="login_username_label",
                label="아이디 라벨",
                default="아이디",
                input_type="text",
            ),
            ContentField(
                key="login_password_label",
                label="비밀번호 라벨",
                default="비밀번호",
                input_type="text",
            ),
            ContentField(
                key="login_submit_label",
                label="로그인 버튼 문구",
                default="로그인",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="boards_common",
        title="게시판 공통 문구",
        description="게시판(기독교 소개, 설교, 성경 공부, 교회 생활 등)에 공통으로 사용되는 문구입니다.",
        fields=[
            ContentField(
                key="board_form_title_placeholder",
                label="게시글 작성 폼 - 제목 입력 안내",
                default="제목",
                input_type="text",
            ),
            ContentField(
                key="board_form_content_placeholder",
                label="게시글 작성 폼 - 내용 입력 안내",
                default="내용 (마크다운 형식 지원: **굵게**, *기울임*, # 제목, ## 부제목, - 목록, 등)",
            ),
            ContentField(
                key="board_form_submit_label",
                label="게시글 작성 폼 - 등록 버튼",
                default="등록하기",
                input_type="text",
            ),
            ContentField(
                key="board_empty_message",
                label="게시글이 없을 때 안내 문구",
                default="게시글이 없습니다.",
                input_type="text",
            ),
            ContentField(
                key="board_posts_section_heading",
                label="기존 게시글 섹션 제목",
                default="기존 게시글",
                input_type="text",
            ),
            ContentField(
                key="board_delete_button_label",
                label="게시글 카드 - 삭제 버튼",
                default="삭제",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="board_intro",
        title="게시판 - 기독교 소개",
        description="기독교 소개 게시판에 사용되는 문구입니다.",
        fields=[
            ContentField(
                key="board_intro_page_heading",
                label="페이지 상단 제목",
                default="기독교 소개 게시판",
                input_type="text",
            ),
            ContentField(
                key="board_intro_form_heading",
                label="게시글 작성 카드 제목",
                default="게시글 작성 (기독교 소개)",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="board_sermons",
        title="게시판 - 설교",
        description="설교 게시판에 사용되는 문구입니다.",
        fields=[
            ContentField(
                key="board_sermons_page_heading",
                label="페이지 상단 제목",
                default="설교 게시판",
                input_type="text",
            ),
            ContentField(
                key="board_sermons_form_heading",
                label="게시글 작성 카드 제목",
                default="게시글 작성 (설교)",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="board_bible_study",
        title="게시판 - 성경 공부",
        description="성경 공부 게시판에 사용되는 문구입니다.",
        fields=[
            ContentField(
                key="board_bible_study_page_heading",
                label="페이지 상단 제목",
                default="성경 공부 게시판",
                input_type="text",
            ),
            ContentField(
                key="board_bible_study_form_heading",
                label="게시글 작성 카드 제목",
                default="게시글 작성 (성경 공부)",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="board_church_life",
        title="게시판 - 교회 생활",
        description="교회 생활 게시판에 사용되는 문구입니다.",
        fields=[
            ContentField(
                key="board_church_life_page_heading",
                label="페이지 상단 제목",
                default="교회 생활 게시판",
                input_type="text",
            ),
            ContentField(
                key="board_church_life_form_heading",
                label="게시글 작성 카드 제목",
                default="게시글 작성 (교회 생활)",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="upload",
        title="자료 공유 페이지",
        description="자료 업로드/다운로드 페이지에 표시되는 문구입니다.",
        fields=[
            ContentField(
                key="upload_page_title",
                label="브라우저 탭 제목",
                default="자료 공유",
                input_type="text",
            ),
            ContentField(
                key="upload_heading",
                label="페이지 상단 제목",
                default="자료 공유",
                input_type="text",
            ),
            ContentField(
                key="upload_uploaded_files_heading",
                label="업로드된 파일 섹션 제목",
                default="업로드된 파일",
                input_type="text",
            ),
            ContentField(
                key="upload_uploaded_at_label",
                label="파일 카드 - 업로드 날짜 라벨",
                default="업로드 날짜",
                input_type="text",
            ),
            ContentField(
                key="upload_view_button",
                label="파일 카드 - 보기 버튼",
                default="보기",
                input_type="text",
            ),
            ContentField(
                key="upload_delete_button",
                label="파일 카드 - 삭제 버튼",
                default="삭제",
                input_type="text",
            ),
            ContentField(
                key="upload_form_file_label",
                label="파일 업로드 폼 - 파일 선택 라벨",
                default="파일 선택",
                input_type="text",
            ),
            ContentField(
                key="upload_form_submit_button",
                label="파일 업로드 폼 - 제출 버튼",
                default="업로드하기",
                input_type="text",
            ),
            ContentField(
                key="upload_success_message",
                label="업로드 성공 알림 문구",
                default="파일 업로드 성공!",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="board_general",
        title="게시판 - 일반",
        description="자유 게시판(게시글 및 채팅) 페이지 문구입니다.",
        fields=[
            ContentField(
                key="board_general_page_title",
                label="브라우저 탭 제목",
                default="게시글 및 채팅",
                input_type="text",
            ),
            ContentField(
                key="board_general_heading",
                label="페이지 상단 제목",
                default="게시글",
                input_type="text",
            ),
            ContentField(
                key="board_general_form_heading",
                label="게시글 작성 카드 제목",
                default="새 게시글 작성",
                input_type="text",
            ),
            ContentField(
                key="board_general_title_label",
                label="게시글 작성 폼 - 제목 라벨",
                default="제목",
                input_type="text",
            ),
            ContentField(
                key="board_general_content_label",
                label="게시글 작성 폼 - 내용 라벨",
                default="내용",
                input_type="text",
            ),
            ContentField(
                key="board_general_submit_label",
                label="게시글 작성 폼 - 등록 버튼",
                default="게시글 등록",
                input_type="text",
            ),
            ContentField(
                key="board_general_guest_notice",
                label="비로그인 안내 문구",
                default="게시글 등록 및 삭제는 관리자 계정으로 로그인 후 이용 가능합니다.",
            ),
            ContentField(
                key="board_general_guest_login_link",
                label="비로그인 안내 - 로그인 링크 텍스트",
                default="로그인하기",
                input_type="text",
            ),
            ContentField(
                key="board_general_posts_heading",
                label="기존 게시글 섹션 제목",
                default="기존 게시글",
                input_type="text",
            ),
            ContentField(
                key="board_general_post_date_label",
                label="게시글 카드 - 작성일 라벨",
                default="작성일",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="meta",
        title="검색 최적화(SEO)",
        description="사이트 전역 기본 메타 태그 문구입니다. 각 페이지에서 별도로 덮어쓸 수도 있습니다.",
        fields=[
            ContentField(
                key="meta_default_keywords",
                label="기본 메타 키워드",
                default="유니버시티 교회, University Church, 메릴랜드 대학, 신앙 공동체, 교회, 예배, 성경 공부",
                input_type="textarea",
            ),
            ContentField(
                key="meta_default_description",
                label="기본 메타 설명",
                default="유니버시티 교회 공식 홈페이지. 50여년간 메릴랜드 대학 가족과 지역 이민사회가 함께 세워 온 신앙 공동체.",
            ),
        ],
    ),
    ContentSection(
        id="footer",
        title="하단 정보",
        description="모든 페이지 하단에 표시되는 고정 문구입니다.",
        fields=[
            ContentField(
                key="footer_contact_heading",
                label="하단 - 연락처 제목",
                default="Get In Touch",
                input_type="text",
            ),
            ContentField(
                key="footer_contact_address",
                label="하단 - 주소",
                default="8108 54th Ave. College Park, MD 20740",
                input_type="textarea",
            ),
            ContentField(
                key="footer_version_heading",
                label="하단 - 버전 정보 제목",
                default="Version Info",
                input_type="text",
            ),
            ContentField(
                key="footer_version_text",
                label="하단 - 버전 안내",
                default="Current Version: 1.0.0",
                input_type="text",
            ),
            ContentField(
                key="footer_version_credit",
                label="하단 - 제작자 표시 (마크다운 허용)",
                default="Developed By [Sueun Cho](https://github.com/sueun-dev)",
                format="markdown",
            ),
            ContentField(
                key="footer_legal_heading",
                label="하단 - 법적 고지 제목",
                default="Legal",
                input_type="text",
            ),
            ContentField(
                key="footer_legal_notice",
                label="하단 - 법적 고지 문구",
                default="Unauthorized use of content prohibited.",
            ),
        ],
    ),
    ContentSection(
        id="home",
        title="메인 페이지",
        description="홈페이지에 노출되는 모든 문구입니다.",
        fields=[
            ContentField(
                key="home_header_highlight",
                label="메인 헤더 강조 텍스트",
                default="University Church",
                input_type="text",
            ),
            ContentField(
                key="home_header_title",
                label="메인 헤더 제목 나머지 부분",
                default="in College Park",
                input_type="text",
            ),
            ContentField(
                key="main_top_welcome",
                label="메인 상단 환영 메시지 (마크다운)",
                default="""**University Church에 오신 것을 환영합니다!**

저희 교회는 하나님 나라의 가치와 사랑을 품고 지역 사회와 세계를 섬기는 공동체입니다. 
함께 신앙의 여정을 걸어가며 성장하고 섬기는 삶을 살아가길 원합니다.""",
                format="markdown",
            ),
            ContentField(
                key="main_church_intro",
                label="메인 교회 소개 (마크다운)",
                default="""University Church는 미국 메릴랜드에 위치한 한인 교회로, 하나님의 말씀과 예배를 통해 
모든 세대가 함께 성장하는 건강한 교회 공동체입니다. 대학가를 중심으로 다양한 연령층이 
함께 예배하고 교제하며 하나님 나라를 확장해가고 있습니다.""",
                format="markdown",
            ),
            ContentField(
                key="home_schedule_section_title",
                label="예배 및 모임 섹션 제목",
                default="예배 및 모임 시간",
                input_type="text",
            ),
            ContentField(
                key="home_schedule_service_1_title",
                label="예배 카드 1 제목",
                default="주일 예배",
                input_type="text",
            ),
            ContentField(
                key="home_schedule_service_1_detail",
                label="예배 카드 1 설명",
                default="매주 주일 오전 11시",
                input_type="text",
            ),
            ContentField(
                key="home_schedule_service_2_title",
                label="예배 카드 2 제목",
                default="성경 공부",
                input_type="text",
            ),
            ContentField(
                key="home_schedule_service_2_detail",
                label="예배 카드 2 설명",
                default="매주 주일 오후 1시",
                input_type="text",
            ),
            ContentField(
                key="home_schedule_service_3_title",
                label="예배 카드 3 제목",
                default="새벽 기도회",
                input_type="text",
            ),
            ContentField(
                key="home_schedule_service_3_detail",
                label="예배 카드 3 설명",
                default="화-토 오전 6시 Zoom",
                input_type="text",
            ),
            ContentField(
                key="home_zoom_button_label",
                label="Zoom 버튼 문구",
                default="새벽 기도회 Zoom",
                input_type="text",
            ),
            ContentField(
                key="home_map_section_title",
                label="지도 섹션 제목",
                default="찾아오는 길",
                input_type="text",
            ),
            ContentField(
                key="home_contact_heading",
                label="Contact 섹션 제목",
                default="Contact Us",
                input_type="text",
            ),
            ContentField(
                key="home_contact_description",
                label="Contact 섹션 설명",
                default="8108 54th Ave. College Park, MD 20740",
                input_type="textarea",
            ),
            ContentField(
                key="home_contact_email_button",
                label="이메일 버튼 텍스트",
                default="이메일",
                input_type="text",
            ),
            ContentField(
                key="home_message_button_label",
                label="목사님께 메시지 버튼",
                default="목사님께 메시지 남기기",
                input_type="text",
            ),
        ],
    ),
    ContentSection(
        id="about",
        title="교회 소개 페이지",
        description="교회 소개 페이지에 노출되는 문구입니다.",
        fields=[
            ContentField(
                key="about_page_title",
                label="브라우저 탭 제목",
                default="About Us - University Church",
                input_type="text",
            ),
            ContentField(
                key="about_page_heading",
                label="페이지 상단 제목",
                default="교회 소개",
                input_type="text",
            ),
            ContentField(
                key="about_vision_heading",
                label="비전 섹션 제목",
                default="비전 선언문",
                input_type="text",
            ),
            ContentField(
                key="about_vision_content",
                label="비전 섹션 내용 (마크다운)",
                default="""- 우리는 하나님 나라의 신앙과 생각과 이상을 품고 세상을 변화시키는 교회입니다.
- 우리는 세상에 감동을 주고 영향을 끼치는 평신도 선교사들을 파송하는 선교적 교회입니다.
- 우리는 지성과 영성을 겸비한 그리스도인 리더를 키우는 교회입니다.
- 우리는 이 이상을 실현하기 위해 훈련 받는 제자 공동체입니다.
- 우리는 하나님 안의 한 지체로서 가족 공동체를 세워 가는 교회입니다.""",
                format="markdown",
            ),
            ContentField(
                key="about_pastor_section_heading",
                label="담임 목사 섹션 제목",
                default="담임 목사 소개",
                input_type="text",
            ),
            ContentField(
                key="about_pastor_profile",
                label="담임 목사 소개 내용 (마크다운)",
                default="""### 김성원 목사

#### 교육 배경
- KAIST 수학
- NYU 수학 PhD (심장 모델링)
- 장신대 MDiv (시리아어 바울 서신)
- GMU 계산생물학 PhD (분자 동역학)

저는 원래 엄밀한 증명과 정교한 계산을 추구하던 수학도였습니다. 그런데 유학생활 중 친구들을 따라 갔던 이민교회에서 갑자기 예수님을 알고 성경을 읽게 되었습니다. 추상적이고 불변하는 형식적 진리를 탐구하던 저에게 성경은 영원하고 초월적이면서도 인격적인, 전혀 새로운 진리의 세계를 열어 주었습니다. 성경의 언어와 역사를 배우는 데 몰두하게 되었고, 그 가르침을 전하는 것이 훨씬 복되고 재미있는 일이 되었습니다.

장신대에서 신학을 배운 후 메릴랜드와 버지니아에서 교육목회를 해 왔고, 교회에서 올바르게 가르쳐야 하는 것들에 대한 정밀과학인 교의학 책들을 열심히 읽고 있습니다. 수학과 자연과학에 지속적인 관심을 가지면서, 그것이 어떻게 신앙과 만나 더 멋진 이야기들을 만들어 내는지를 상상합니다. 아내 이은정과 세 자녀와 함께 복된 믿음의 길을 가고 있으며, 강아지와 파인애플과 오페라를 좋아합니다.

신앙을 갖게 된 후 저의 한결같은 관심은, 현대 지성인들에게 예수님의 복음을 효과적으로 전하는 것입니다. 지식과 정보가 넘치는 이 시대이지만, 예수님이 1세기 로마제국의 유대 지방에서 십자가에 죽으시고 부활하신 역사, 목적, 의미를 대중에게 정확히 알려 주는 자료는 의외로 빈약합니다. 전능자에 대한 신앙을 갖는 것은 개인의 고유한 인격적 경험이지만, 그것을 위해 기독교가 정말로 무엇을 말하는지, 예수님이 얼마나 멋진 분이신지를 전해 드리는 역할을 하고 싶습니다.""",
                format="markdown",
            ),
        ],
    ),
    ContentSection(
        id="message",
        title="메시지 페이지",
        description="목사님께 연락하기 페이지의 안내 문구와 라벨을 설정합니다.",
        fields=[
            ContentField(
                key="message_page_title",
                label="브라우저 탭 제목",
                default="메시지 남기기 - University Church",
                input_type="text",
            ),
            ContentField(
                key="message_heading",
                label="페이지 상단 제목",
                default="목사님께 메시지 남기기",
                input_type="text",
            ),
            ContentField(
                key="message_name_label",
                label="이름 라벨",
                default="이름",
                input_type="text",
            ),
            ContentField(
                key="message_email_label",
                label="이메일 라벨",
                default="이메일 (선택사항)",
                input_type="text",
            ),
            ContentField(
                key="message_email_placeholder",
                label="이메일 입력 안내 문구",
                default="답변을 받길 원하시면 이메일을 입력해주세요",
                input_type="text",
            ),
            ContentField(
                key="message_email_help",
                label="이메일 도움말",
                default="이메일은 답변을 드리기 위한 용도로만 사용됩니다.",
            ),
            ContentField(
                key="message_subject_label",
                label="제목 라벨",
                default="제목",
                input_type="text",
            ),
            ContentField(
                key="message_content_label",
                label="메시지 내용 라벨",
                default="메시지 내용",
                input_type="text",
            ),
            ContentField(
                key="message_submit_label",
                label="전송 버튼 문구",
                default="메시지 보내기",
                input_type="text",
            ),
            ContentField(
                key="message_footer_notice",
                label="페이지 하단 안내 문구",
                default="보내신 메시지는 목사님께 전달됩니다. 답변이 필요하신 경우 이메일을 남겨주세요.",
            ),
        ],
    ),
]


def _flatten_sections(sections: Iterable[ContentSection]) -> Dict[str, ContentField]:
    lookup: Dict[str, ContentField] = {}
    for section in sections:
        for field in section.fields:
            lookup[field.key] = field
    return lookup


FIELD_LOOKUP: Dict[str, ContentField] = _flatten_sections(SECTION_DEFINITIONS)


def iter_sections() -> Iterable[ContentSection]:
    """Iterate over defined sections."""
    return SECTION_DEFINITIONS


def get_field(key: str) -> Optional[ContentField]:
    """Return metadata for a given content key."""
    return FIELD_LOOKUP.get(key)


def get_default_for_key(key: str) -> str:
    """Return the default content registered for the key."""
    field = get_field(key)
    return field.default if field else ""
