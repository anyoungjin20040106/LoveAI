import google.generativeai as genai
from fastapi import FastAPI,Form,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import markdown
import os
genai.configure(api_key=os.getenv("Gemini"))
model = genai.GenerativeModel("gemini-1.5-flash")
app=FastAPI()
templates=Jinja2Templates("templates")
app.mount("/Asset", StaticFiles(directory="Asset"))
@app.get("/")
def index():
    return FileResponse("index.html")
@app.post("/result")
def result(request:Request,name:str=Form(...),sex:str=Form(...),birthday:str=Form(None),type:str=Form(...),m1:str=Form(None),m2:str=Form(None),m3:str=Form(None),m4:str=Form(None)):
    text=f"안녕 너는 연애운을 봐주는 점술사야 성별이 {sex}이고 "
    if birthday:
        y,m,d=birthday.split("-")
        text+=f"{y}년 {m}월 {d}일에 태어난"
    else:
        text+=f"MBTI가 {''.join([m1,m2,m3,m4])}인"
    text+=f" {name}의 {datetime.today().strftime('%Y년%m월%d일')}의 연애운을 봐줘, 그사람은 {type}이며 그사람의 장점, 단점을 말해주고 "
    text+="연인이 생기는 "if type=="솔로" else f"현제 {name}의 연인 관계는 어떤지 사주로 평가해주고 더 좋은 관계가 돼기 위한 "
    text+="운세를 알려줘"
    print(text)
    response = model.generate_content(text)
    result=markdown.markdown(response.text)
    return templates.TemplateResponse("result.html",{"request":request,"result":result,"name":name})