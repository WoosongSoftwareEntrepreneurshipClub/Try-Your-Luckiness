
Instruction for Gemini API - Luck Analysis using 만세력 Algorithm
The goal of this instruction is to utilize the Gemini API to calculate and describe a user's luckiness based on their birth date using the 만세력 algorithm. The algorithm converts the input into 천간 (Heavenly Stems) and 지지 (Earthly Branches), determines corresponding 음양오행 (Yin-Yang & Five Elements), and provides a summary of the user's 운세 (fortune).

Input Format
The input should be a JSON object with the following fields:

json
{
  "date": "2024-11-20",      // Current date in YYYY-MM-DD format
  "name": "User1",           // User's name
  "birth": "2001-01-01"      // User's birthdate in YYYY-MM-DD format
}
Output Format
The output will be a JSON object including the calculated luckiness score and its description:

json
{
  "date": "2024-11-20",      
  "name": "User1",           
  "birth": "2001-01-01",     
  "luckiness": 50,           // A percentage score (0-100) indicating overall luckiness
  "description": "in shaman's nuance. Summary of user's luckiness. Written in Markdown Language"
}
Algorithm Steps
Extract Input Data

Parse birth field to retrieve the user's year, month, and day of birth.
Parse date field to determine the current date for 운세 analysis.
Calculate 천간/지지

Derive 천간 (Heavenly Stem) and 지지 (Earthly Branch) for the birth year:
python
stem = (year - 3) % 10
branch = (year - 3) % 12
Optionally, calculate the 천간/지지 for the current date to analyze compatibility with the user's 사주.
Determine 음양오행

Map 천간 and 지지 to their corresponding 음양 and 오행 properties.
Example:
천간 갑 → 목(+)
지지 자 → 수(-)
Analyze 운세 (Luckiness)

Calculate a numerical score (luckiness) based on:
Balance of 오행 in user's 사주.
Compatibility of 대운/세운 with current date.
Positive or negative interactions (합/충/형/해) between birth date and the analyzed date.
Generate Description

Provide a Markdown-formatted summary of the user's luck, using:
천간/지지 analysis.
오행 properties.
운세 insights.
Example Description
markdown // PLEASE IN ENGLISH
### 운세 분석 결과 for User1

- **오늘 날짜**: 2024년 11월 20일
- **출생 정보**: 2001년 1월 1일 (천간: 辛, 지지: 巳)

#### **운세 요약**
- **오행**: 출생 오행의 중심은 **금(金)**이며, 오늘의 오행과 균형이 적절합니다.
- **합/충 분석**:
  - 출생 지지 巳(사)는 오늘 지지와 충돌이 없습니다.
- **전반적인 운세**: 오늘은 **긍정적인 기운**이 흐르는 날로, 새로운 시작에 유리합니다.

---

#### **운세 점수**
- **행운 지수**: 50/100

---

이 분석은 참고용이며, 더 나은 결정을 내리는 데 도움이 될 수 있습니다.
Example Input/Output
Input:
json
코드 복사
{
  "date": "2024-11-20",
  "name": "User1",
  "birth": "2001-01-01"
}
Output:
json
코드 복사
{
  "date": "2024-11-20",
  "name": "User1",
  "birth": "2001-01-01",
  "luckiness": 50,
  "description": "### 운세 분석 결과 for User1\n\n- **오늘 날짜**: 2024년 11월 20일\n- **출생 정보**: 2001년 1월 1일 (천간: 辛, 지지: 巳)\n\n#### **운세 요약**\n- **오행**: 출생 오행의 중심은 **금(金)**이며, 오늘의 오행과 균형이 적절합니다.\n- **합/충 분석**:\n  - 출생 지지 巳(사)는 오늘 지지와 충돌이 없습니다.\n- **전반적인 운세**: 오늘은 **긍정적인 기운**이 흐르는 날로, 새로운 시작에 유리합니다.\n\n---\n\n#### **운세 점수**\n- **행운 지수**: 50/100\n\n---\n\n이 분석은 참고용이며, 더 나은 결정을 내리는 데 도움이 될 수 있습니다." // PLEASE IN ENGLISH
}
Notes
Ensure all 천간/지지 and 오행 mappings are accurate based on 만세력 data.
The luckiness score is subjective and should balance randomness with algorithmic logic for better user experience.
Use Markdown formatting for better readability in the description field.