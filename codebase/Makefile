PYTHON = .venv/Scripts/python.exe

.PHONY: bot test seed eval eval-gia thu-hoi help

help:
	@echo.
	@echo   make bot                        Khoi dong Spidey (bot Discord)
	@echo   make test                       Chay 115 unit test, khong can API key
	@echo   make seed                       Nap 20 tin nhan gia vao index.db
	@echo   make eval-gia                   Kiem tra runner bang LLM gia
	@echo   make eval                       Chay tron bo 22 case golden set
	@echo   make thu-hoi q="link slide 5"   Hoi 1 cau tu terminal
	@echo.

bot:
	$(PYTHON) -m timlai.bot

test:
	$(PYTHON) -m pytest tests -q

seed:
	$(PYTHON) scripts/seed_gia.py

eval-gia:
	$(PYTHON) scripts/chay_eval.py --gia

eval:
	$(PYTHON) scripts/chay_eval.py

thu-hoi:
	$(PYTHON) scripts/thu_hoi.py "$(q)"
