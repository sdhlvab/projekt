# 🕹️ Hackerman vs Bugzilla – Instalacja gry (Windows)

Witaj, graczu! Jeśli chcesz zagrać w terminalową przygodę **„Hackerman vs Bugzilla”** na Windowsie, poniżej znajdziesz prostą instrukcję krok po kroku.

---

## 📦 Wymagania

- ✅ **Windows 10/11**
- ✅ **Python 3.10+** (zalecane 3.12)
- ✅ **Pip** (menedżer pakietów Pythona)
- ✅ **Git** (opcjonalnie – do pobrania repo)

---

## 🐍 Instalacja Pythona (jeśli jeszcze nie masz)

1. Wejdź na oficjalną stronę: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Pobierz instalator Python 3.x (np. `Python 3.12.x`)
3. **Podczas instalacji zaznacz koniecznie:**
   - ✅ *Add Python to PATH*
   - ✅ *Install pip*
4. Kliknij **Install Now**
5. Po zakończeniu instalacji uruchom terminal (CMD / PowerShell) i wpisz:

```bash
python --version
```

Powinno pokazać: `Python 3.x.x`

---

## 🚀 Instalacja gry krok po kroku

### 1️⃣ Pobierz projekt

#### ✅ Opcja A – przez Git (gra zostanie ściągnięta do katalogu, w którym aktualnie jesteś) :
```bash
git clone https://github.com/sdhlvab/projekt.git
cd projekt
```

#### ✅ Opcja B – jako ZIP:
1. Wejdź na: [https://github.com/sdhlvab/projekt](https://github.com/sdhlvab/projekt)
2. Kliknij zielony przycisk **Code → Download ZIP**
3. Wypakuj ZIPa gdziekolwiek chcesz (np. na pulpit)

---

### 2️⃣ Zainstaluj wymagane biblioteki

W katalogu z grą uruchom terminal (PowerShell lub CMD):

```bash
pip install -r requirements.txt
```

📦 Jeśli nie masz pliku `requirements.txt`, możesz zainstalować najważniejszą bibliotekę ręcznie:

```bash
pip install pygame
```

---

### 3️⃣ Uruchom grę

W terminalu, będąc w katalogu z plikiem `main.py`, wpisz:

```bash
python main.py
```

---

## 🎮 Sterowanie w grze

- ⬅️➡️ 🔼🔽 – poruszanie się Hackermana
- ␣ **Spacja** – atak
- ⎋ **Escape** – pauza
- 🎵 **M** – włącz/wyłącz muzykę

---

## ❓ Problemy?

- ❗ **Błąd `pygame`?** – sprawdź, czy został poprawnie zainstalowany (`pip install pygame`)
- ❗ **Gra nie startuje?** – sprawdź, czy uruchamiasz w katalogu, gdzie znajduje się `main.py`
- ❗ **Brak grafiki lub dźwięku?** – upewnij się, że katalog `assets/` jest obecny i zawiera wszystkie wymagane pliki

---

## ❤️ Autorzy

- 👨‍💻 Kamil S.
- 🎨 Grafiki: AI, Paint
- 🎵 Dźwięki: pixabay,com

---

Miłej zabawy! 🎉
