# PygeTurner

## Uruchamianie

Poniższe polecenia są odpowiednie dla systemu Windows. Na innych systemach, takich jak Linux czy Mac, należy stosować poniższe polecenia w składni odpowiedniej dla powłoki tych systemów.

### 1. Instalacja Pythona
Należy w systemie operacyjnym zainstalować środowisko Python w wersji 3.10 lub wyższej, choć działanie w wyższych wersjach nie jest zagwarantowane. Są na to różne sposoby, przykładowo:
* za pomocą Microsoft Store, lub
* można pobrać program instalacyjny z zaufanych stron, w tym oficjalnej strony Pythona, lub
* używając narzędzi takich jak Anaconda czy Chocolatey.

Po szczegóły odsyłam do materiałów dostępnych w Internecie.

### 2. Przygotowanie środowiska wirtualnego Pythona
W konsoli PowerShell należy uruchomić poniższe polecenia:
* Stworzenie środowiska wirtualnego:
  ```bat
  python3.10 -m venv .venv_Windows
  ```
* Uaktywnienie środowiska wirtualnego:
  ```bat
  .venv_Windows\Scripts\Activate.ps1
  ```
* Instalacja zależności
  ```bat
  pip install -r requirements.txt
  ```

### 3. Uruchamianie aplikacji
W aktywnym środowisku wirtualnym należy uruchomić poniższe polecenie:
```bat
python src\main.py
```

## Aktualizacja zależności
W aktywnym środowisku wirtualnym należy uruchomić poniższe polecenia:
* Instalacja narzędzi `piptools`
  ```bat
  pip install pip-tools
  ```
* Aktualizacja pliku zależności `requiremens.txt`
  ```bat
  pip-compile.exe --upgrade --output-file requirements.txt requirements.in 
  ```
* Instalacja odświeżonych zależności
  ```bat
  pip-sync.exe requirements.txt
  ```