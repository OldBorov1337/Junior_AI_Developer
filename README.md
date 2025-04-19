# Junior_AI_Developer
An application for detecting body position (pose estimation) on `.mp4` video, using a ready-made **MediaPipe** model.

Dla każdej klatki wideo aplikacja:
- wykrywa punkty kluczowe (np. nos, oczy, ramiona, biodra itd.),
- zapisuje współrzędne do pliku `.json`,
- tworzy nowe wideo z zaznaczonymi punktami (szkielet ciała).

Jak uruchomić (bez Dockera):

1. Stwórz i aktywuj wirtualne środowisko:

python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/macOS

2. Zainstaluj wymagane biblioteki:

pip install -r requirements.txt

3. Uruchom aplikację:

python detect.py 1.mp4 result.json

1.mp4 – wejściowe wideo

result.json – plik wyjściowy z punktami

result_with_skeleton.mp4 – wideo z wizualizacją

Jak uruchomić (z Docker):

docker build -t pose-estimation .

docker run -v ${PWD}:/app pose-estimation 1.mp4 result.json
