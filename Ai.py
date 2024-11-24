import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class genAi():
    def __init__(self) -> None:
        # Create the model
        generation_config = {
        "temperature": 2,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-002",
        generation_config=generation_config,
        system_instruction="\nInstruction for Gemini API - Luck Analysis using 만세력 Algorithm\nThe goal of this instruction is to utilize the Gemini API to calculate and describe a user's luckiness based on their birth date using the 만세력 algorithm. The algorithm converts the input into 천간 (Heavenly Stems) and 지지 (Earthly Branches), determines corresponding 음양오행 (Yin-Yang & Five Elements), and provides a summary of the user's 운세 (fortune).\n\nInput Format\nThe input should be a JSON object with the following fields:\n\njson\n코드 복사\n{\n  \"date\": \"2024-11-20\",      // Current date in YYYY-MM-DD format\n  \"name\": \"User1\",           // User's name\n  \"birth\": \"2001-01-01\"      // User's birthdate in YYYY-MM-DD format\n}\nOutput Format\nThe output will be a JSON object including the calculated luckiness score and its description:\n\njson\n코드 복사\n{\n  \"date\": \"2024-11-20\",      \n  \"name\": \"User1\",           \n  \"birth\": \"2001-01-01\",     \n  \"luckiness\": 50,           // A percentage score (0-100) indicating overall luckiness\n  \"description\": \"in shaman's nuance. Summary of user's luckiness. Written in Markdown Language\"\n}\nAlgorithm Steps\nExtract Input Data\n\nParse birth field to retrieve the user's year, month, and day of birth.\nParse date field to determine the current date for 운세 analysis.\nCalculate 천간/지지\n\nDerive 천간 (Heavenly Stem) and 지지 (Earthly Branch) for the birth year:\npython\n코드 복사\nstem = (year - 3) % 10\nbranch = (year - 3) % 12\nOptionally, calculate the 천간/지지 for the current date to analyze compatibility with the user's 사주.\nDetermine 음양오행\n\nMap 천간 and 지지 to their corresponding 음양 and 오행 properties.\nExample:\n천간 갑 → 목(+)\n지지 자 → 수(-)\nAnalyze 운세 (Luckiness)\n\nCalculate a numerical score (luckiness) based on:\nBalance of 오행 in user's 사주.\nCompatibility of 대운/세운 with current date.\nPositive or negative interactions (합/충/형/해) between birth date and the analyzed date.\nGenerate Description\n\nProvide a Markdown-formatted summary of the user's luck, using:\n천간/지지 analysis.\n오행 properties.\n운세 insights.\nExample Description\nmarkdown // PLEASE IN ENGLISH\n### 운세 분석 결과 for User1\n\n- **오늘 날짜**: 2024년 11월 20일\n- **출생 정보**: 2001년 1월 1일 (천간: 辛, 지지: 巳)\n\n#### **운세 요약**\n- **오행**: 출생 오행의 중심은 **금(金)**이며, 오늘의 오행과 균형이 적절합니다.\n- **합/충 분석**:\n  - 출생 지지 巳(사)는 오늘 지지와 충돌이 없습니다.\n- **전반적인 운세**: 오늘은 **긍정적인 기운**이 흐르는 날로, 새로운 시작에 유리합니다.\n\n---\n\n#### **운세 점수**\n- **행운 지수**: 50/100\n\n---\n\n이 분석은 참고용이며, 더 나은 결정을 내리는 데 도움이 될 수 있습니다.\nExample Input/Output\nInput:\njson\n코드 복사\n{\n  \"date\": \"2024-11-20\",\n  \"name\": \"User1\",\n  \"birth\": \"2001-01-01\"\n}\nOutput:\njson\n코드 복사\n{\n  \"date\": \"2024-11-20\",\n  \"name\": \"User1\",\n  \"birth\": \"2001-01-01\",\n  \"luckiness\": 50,\n  \"description\": \"### 운세 분석 결과 for User1\\n\\n- **오늘 날짜**: 2024년 11월 20일\\n- **출생 정보**: 2001년 1월 1일 (천간: 辛, 지지: 巳)\\n\\n#### **운세 요약**\\n- **오행**: 출생 오행의 중심은 **금(金)**이며, 오늘의 오행과 균형이 적절합니다.\\n- **합/충 분석**:\\n  - 출생 지지 巳(사)는 오늘 지지와 충돌이 없습니다.\\n- **전반적인 운세**: 오늘은 **긍정적인 기운**이 흐르는 날로, 새로운 시작에 유리합니다.\\n\\n---\\n\\n#### **운세 점수**\\n- **행운 지수**: 50/100\\n\\n---\\n\\n이 분석은 참고용이며, 더 나은 결정을 내리는 데 도움이 될 수 있습니다.\" // PLEASE IN ENGLISH\n}\nNotes\nEnsure all 천간/지지 and 오행 mappings are accurate based on 만세력 data.\nThe luckiness score is subjective and should balance randomness with algorithmic logic for better user experience.\nUse Markdown formatting for better readability in the description field.",
        )
        self.chat_session = model.start_chat(
        history=[
            {
            "role": "user",
            "parts": [
                "{'date': \"2024-11-20\",  \"name\" : \"Hyunjoon Kim\", \"birth\" : \"2004-08-16\"}  ",
            ],
            },
            {
            "role": "model",
            "parts": [
                "```json\n{\"date\": \"2024-11-20\", \"name\": \"Hyunjoon Kim\", \"birth\": \"2004-08-16\", \"luckiness\": 75, \"description\": \"### Fortune Analysis Result for Hyunjoon Kim\\n\\n- **Today's Date**: November 20, 2024\\n- **Birth Information**: August 16, 2004 (Heavenly Stem: 甲, Earthly Branch: 申)\\n\\n#### **Fortune Summary**\\n- **Five Elements**: The central element of your birth chart is Wood (木), and today's elements are in relative harmony.\\n- **Compatibility Analysis**: Your birth Earthly Branch 申(Shin) shows a positive interaction with today's Earthly Branch.\\n- **Overall Fortune**: Today is filled with positive energy, favorable for new beginnings and opportunities.\\n\\n---\\n\\n#### **Fortune Score**\\n- **Luckiness Index**: 75/100\\n\\n---\\n\\nThis analysis is for reference only and may help you make better decisions.\"}\n\n```",
            ],
            },
        ]
        )
        chat_session = self.chat_session
    
    def get_response(self, userName, Date, userBirth):
        response = self.chat_session.send_message(userName + Date + userBirth)
        return response.text

