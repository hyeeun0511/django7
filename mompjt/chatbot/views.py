from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import json

# 1. 여기에 본인의 API 키를 넣어주세요
GOOGLE_API_KEY = "AIzaSyDSAolHRi9TvnJi9RuC5DYNBDkzVEs_8tY"
genai.configure(api_key=GOOGLE_API_KEY)

def chatbot_view(request):
    if request.method == 'POST':
        try:
            # 데이터 받기
            data = json.loads(request.body)
            user_message = data.get('message', '')
            print(f"▶ 사용자 질문: {user_message}")

            # 2. 모델 이름 변경 (사용자 목록에 있는 최신 모델로 변경)
            # 목록에서 확인된 'gemini-2.5-flash'를 사용합니다.
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # 시스템 프롬프트 (챗봇의 성격 설정)
            system_prompt = "당신은 육아 커뮤니티 '맘스로그'의 친절한 AI 상담사입니다. 답변은 친절하고 따뜻한 말투로 해주세요."
            full_prompt = f"{system_prompt}\n\n사용자 질문: {user_message}"

            # 3. 질문 보내기
            response = model.generate_content(full_prompt)
            ai_response = response.text
            
            print(f"▶ AI 답변 생성 성공: {ai_response[:20]}...")

            return JsonResponse({'response': ai_response})

        except Exception as e:
            print(f"!!!!!! 에러 발생 !!!!!! : {e}")
            return JsonResponse({'response': '죄송합니다. 오류가 발생했어요.'}, status=500)

    return render(request, 'chatbot/chatbot_widget.html')