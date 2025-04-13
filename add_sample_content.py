from app import create_app, db
from app.models import SiteContent

def add_sample_content():
    app = create_app()
    with app.app_context():
        # 기존 콘텐츠 삭제 (새로 시작)
        SiteContent.query.delete()
        
        # 메인 페이지 - 상단 환영 메시지
        welcome = SiteContent(
            key='main_top_welcome',
            title='메인 페이지 - 상단 환영 메시지',
            content="""**University Church에 오신 것을 환영합니다!**

저희 교회는 하나님 나라의 가치와 사랑을 품고 지역 사회와 세계를 섬기는 공동체입니다. 
함께 신앙의 여정을 걸어가며 성장하고 섬기는 삶을 살아가길 원합니다."""
        )
        db.session.add(welcome)
        
        # 메인 페이지 - 교회 간략 소개
        main_intro = SiteContent(
            key='main_church_intro',
            title='메인 페이지 - 교회 간략 소개',
            content="""University Church는 미국 메릴랜드에 위치한 한인 교회로, 하나님의 말씀과 예배를 통해 
모든 세대가 함께 성장하는 건강한 교회 공동체입니다. 대학가를 중심으로 다양한 연령층이 
함께 예배하고 교제하며 하나님 나라를 확장해가고 있습니다."""
        )
        db.session.add(main_intro)
        
        # 교회 소개 페이지 - 상세 소개
        about = SiteContent(
            key='about_page_intro',
            title='교회 소개 페이지 - 상세 소개',
            content="""## University Church 소개

저희 교회는 대학가를 중심으로 젊은이들과 가족들이 함께 모여 예배하고 배우며 섬기는 공동체입니다. 
다양한 배경과 연령대의 교인들이 함께 어우러져 그리스도의 사랑을 나누고 있습니다.

### 우리의 가치

- **말씀 중심**: 성경 말씀을 깊이 배우고 삶에 적용합니다
- **예배와 기도**: 진실한 예배와 중보기도를 통해 하나님과 교제합니다
- **공동체 사랑**: 서로 돌보고 격려하며 사랑의 공동체를 이룹니다
- **선교와 봉사**: 지역사회와 세계를 향한 하나님의 사랑을 실천합니다"""
        )
        db.session.add(about)
        
        # 모든 페이지 - 예배 시간 정보
        service_times = SiteContent(
            key='global_service_times',
            title='예배 시간 정보 (모든 페이지)',
            content="""### 예배 시간 안내

- **주일 예배**: 매주 일요일 오전 11시
- **수요 예배**: 매주 수요일 저녁 7시 30분
- **새벽 기도회**: 화-토 오전 6시 (Zoom)
- **성경 공부**: 매주 주일 오후 1시"""
        )
        db.session.add(service_times)
        
        # 모든 페이지 - 하단 연락처 정보
        footer_contact = SiteContent(
            key='global_footer_contact',
            title='하단부 연락처 정보 (모든 페이지)',
            content="""### 연락처

**주소**: 1234 University Blvd, College Park, MD 20742  
**전화**: (123) 456-7890  
**이메일**: contact@universitychurch.org  
**주일 예배**: 매주 일요일 오전 11시"""
        )
        db.session.add(footer_contact)
        
        # 교회 망사님 인사말
        pastor_message = SiteContent(
            key='about_page_pastor_message',
            title='교회 소개 페이지 - 망사님 인사말',
            content="""## 망사님 인사말

저희 교회를 찾아주셔서 감사합니다. University Church는 하나님의 말씀을 통해 생명의 변화를 경험하고, 
그리스도의 사랑을 삶으로 살아내는 공동체입니다. 예수님의 청부하심처럼 함께 하나님 나라를 크게 꾸며 걸어가는 
모험에 동참해 주시길 이 자리를 통해 초청합니다.

길 목사 올림"""
        )
        db.session.add(pastor_message)
        db.session.add(service_times)
        
        db.session.commit()
        print("샘플 콘텐츠가 성공적으로 추가되었습니다!")

if __name__ == "__main__":
    add_sample_content()
