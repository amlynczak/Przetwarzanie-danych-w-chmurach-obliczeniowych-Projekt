$requirements = "requirements.txt"
if (Test-Path $requirements) {
    pip install -r $requirements
}
python -m uvicorn app.main:app --reload