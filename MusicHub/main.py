from fastapi import FastAPI, UploadFile, BackgroundTasks, Request, HTTPException
from MusicHub.core.config import settings

from MusicHub.emailProvider.emailService import send_email
from MusicHub.emailProvider.email import register_template_body
from MusicHub.aws.bucket import upload_to_bucket
from MusicHub.models import user
from MusicHub.db.db import engine
from MusicHub.logger import LoggerMiddleware


user.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)


app.add_middleware(LoggerMiddleware, info_file="info.log", error_file="errors.log")


# Test endpoints to check functionality


@app.get("/test-email")
async def test_send_mail(background_tasks: BackgroundTasks):

    background_tasks.add_task(
        send_email,
        "Finish your registration",
        ["Damian.Bednarek@itechart-group.com"],
        register_template_body("Damian", "link"),
    )
    return "Success"


@app.post("/test-aws")
def test_upload_file(file: UploadFile, background_tasks: BackgroundTasks):

    background_tasks.add_task(upload_to_bucket, file)
    return "success"


@app.get("/error")
def test_error():

    return 1 / 0
