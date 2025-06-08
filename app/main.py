from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

app = FastAPI()

# 정적 파일과 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


# 기본 라우트 (로그인 페이지)
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 로그인 처리
@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    password = form_data.get("password")

    if password == "4568":
        request.session["authenticated"] = True
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        raise HTTPException(status_code=401, detail="잘못된 비밀번호입니다")


# 대시보드 페이지
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/")
    return templates.TemplateResponse("dashboard.html", {"request": request})