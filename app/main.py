from fastapi import FastAPI

app=FastAPI(title="MailGent")

@app.get("/health")
def health():
    return{"status":"ok","service":"MailGent"}
