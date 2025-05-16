### GEMINI로 메일 초안 작성해주는 서버 ###

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # .env 파일에 GEMINI_API_KEY 등을 넣어 두세요

GEMINI_MODEL = "gemini-2.5-pro-preview-05-06"  # 필요 시 다른 버전으로 교체
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)


import uvicorn
import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# 1. 루트 경로 (GET)
# ------------------------------
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

# ------------------------------
# 2. POST 요청 처리 예제
# ------------------------------
class UserInput(BaseModel):
    name: str
    age: int

# 실험용용
@app.get("/hello")
async def say_hello():
	
	return "hello\nhi"

@app.get("/gen-mail-form")
async def autogeneration(situation: str, sender: str, reciever: str):
	prompt = f"""
상황: {situation}
보내는 사람: {sender}
받는 사람: {reciever}
상황에 맞게 받는 사람에게 메일 초안을 작성해줘.
개행의 경우 HTML 형식에 맞게 작성해줘.
	"""
	model = genai.GenerativeModel(GEMINI_MODEL)
	
	loop = asyncio.get_event_loop()
	response = await loop.run_in_executor(None, model.generate_content, prompt)

	print(response.text)
	return response.text

@app.post("/greet")
async def greet_user(user: UserInput):
    return {
        "message": f"Hello {user.name}, you are {user.age} years old!"
    }

# ------------------------------
# 3. 요청 헤더/본문 보기 (디버그용)
# ------------------------------
@app.post("/echo")
async def echo(request: Request):
    body = await request.json()
    headers = dict(request.headers)
    return {"headers": headers, "body": body}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)