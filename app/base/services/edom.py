from functools import lru_cache
from pathlib import Path
import pickle

INSTRUCTOR_CHOICES = (
    "David Bani Adam, S.H, M.H",
    "Muhammad Fikri Hidayattullah, S.T., M.Kom.",
    "Hendrawan Aprilia A, S.T.",
    "Priyanto Tamami, S.Kom.",
    "M. Nishom, M.Kom.",
    "Dwi Intan Af'idah, M.Kom.",
    "Mirza Alim Mutasodirin, M.Kom",
    "Ardi Susanto, S.Kom., M.Cs.",
    "Riszki Wijayatun Pratiwi., M.CS.",
    "Ary Herijanto, S.Kom, MMSi",
    "Romi Muharyono, S.Ag.",
    "Hepatika Zidny Ilmadina, S.Pd., M.Kom.",
    "Sharfina Febbi Handayani, M.Kom.",
    "Ginanjar Wiro Sasmito, M.Kom.",
    "Taufiq Abidin, M.Kom.",
    "Dega Surono Wibowo, S.T., M.Kom.",
    "Dairoh, M.Sc.",
    "Slamet Wiyono, S.Pd., M. Eng.",
    "Muchammad Sofyan Firmansyah, S.S, M.A",
    "Aris Setyawan, S.T",
    "Rosid Mustofa, M.Kom",
    "Dyah Apriliani, S.T., M.Kom.",
)

_INSTRUCTORS_BY_SEMESTER = {
    "2": {
        "A": (15, 8, 16, 17, 10, 9, 12, 18, 0),
        "B": (15, 8, 16, 17, 10, 9, 12, 18, 0),
        "C": (7, 8, 16, 17, 10, 9, 5, 18, 0),
        "D": (7, 8, 16, 17, 10, 9, 5, 18, 0),
    },
    "4": {"*": (4, 15, 3, 14, 21, 11, 1)},
    "6": {
        "A": (20, 2, 19, 8, 12, 7, 6, 5),
        "B": (20, 2, 19, 8, 12, 7, 6, 5),
        "C": (20, 2, 19, 8, 12, 7, 6, 13),
        "D": (20, 2, 19, 8, 12, 7, 6, 13),
    },
    "8": {"*": (14, 16)},
}


def instructors_for(semester, class_name):
    choices = _INSTRUCTORS_BY_SEMESTER.get(str(semester), {})
    indices = choices.get(str(class_name).upper(), choices.get("*", ()))
    return [INSTRUCTOR_CHOICES[index] for index in indices]


@lru_cache(maxsize=1)
def _load_model_and_tokenizer():
    from tensorflow.keras.models import load_model

    base_dir = Path(__file__).resolve().parents[1]
    with (base_dir / "tokenizer1.pickle").open("rb") as tokenizer_file:
        tokenizer = pickle.load(tokenizer_file)
    model = load_model(str(base_dir / "best_model.h5"))
    return model, tokenizer


def predict_sentiment(text):
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    model, tokenizer = _load_model_and_tokenizer()
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, padding="post", maxlen=50)
    scores = model.predict(padded_sequence, verbose=0)[0]
    labels = ("Baik", "Cukup", "Kurang", "Sangat Baik")
    index = int(scores.argmax())
    return labels[index], float(scores[index])
