import datetime

# 15 Shlokas with translations
shlokas = [
    {
        "en": "O Lord, protect me always like a shield in battle.",
        "te": "ఓ ప్రభూ, యుద్ధంలో కవచంలా నన్ను ఎప్పుడూ రక్షించు.",
        "hi": "हे प्रभु, युद्ध में ढाल की तरह मेरी हमेशा रक्षा करें।"
    },
    {
        "en": "May all beings be happy; may all be free from disease.",
        "te": "అన్ని జీవులు సంతోషంగా ఉండగలుగునుగాక; అనారోగ్యం లేకుండా ఉండుగాక.",
        "hi": "सभी प्राणी सुखी हों; सभी रोग से मुक्त हों।"
    },
    {
        "en": "Truth alone triumphs, not falsehood.",
        "te": "నిజమే గెలుస్తుంది, అబద్ధం కాదు.",
        "hi": "सत्य ही विजयी होता है, असत्य नहीं।"
    },
    {
        "en": "Do your duty without attachment to results.",
        "te": "ఫలితాల పట్ల ఆకర్షణ లేకుండా నీ కర్తవ్యాన్ని చేయి.",
        "hi": "परिणामों से जुड़े बिना अपना कर्तव्य निभाओ।"
    },
    {
        "en": "Even the strongest fall without wisdom.",
        "te": "జ్ఞానం లేకపోతే బలవంతులైన వారుకూడా పడిపోతారు.",
        "hi": "बुद्धि के बिना सबसे शक्तिशाली भी गिर जाते हैं।"
    },
    {
        "en": "One's own duty, though imperfect, is better than another's duty well performed.",
        "te": "పరిపూర్ణంగా చేసిన పరధర్మం కన్నా, లోపంగా చేసిన స్వధర్మమే ఉత్తమం.",
        "hi": "दूसरों का धर्म भलीभांति निभाने से अच्छा है अपना धर्म निभाना, भले वह अपूर्ण हो।"
    },
    {
        "en": "He who controls his mind is the true conqueror.",
        "te": "తన మనసును నియంత్రించుకున్నవాడే నిజమైన విజేత.",
        "hi": "जो अपने मन को नियंत्रित करता है वही सच्चा विजेता है।"
    },
    {
        "en": "Time is the greatest healer.",
        "te": "కాలమే గొప్ప వైద్యుడు.",
        "hi": "समय सबसे बड़ा उपचारक है।"
    },
    {
        "en": "Knowledge removes darkness of ignorance.",
        "te": "జ్ఞానం అజ్ఞాన అంధకారాన్ని తొలగిస్తుంది.",
        "hi": "ज्ञान अज्ञानता के अंधकार को दूर करता है।"
    },
    {
        "en": "Where there is righteousness, there is victory.",
        "te": "ధర్మం ఉన్నచోటే విజయముంది.",
        "hi": "जहाँ धर्म है, वहाँ विजय है।"
    },
    {
        "en": "Non-violence is the highest virtue.",
        "te": "అహింసే అత్యున్నత ధర్మం.",
        "hi": "अहिंसा सबसे बड़ा धर्म है।"
    },
    {
        "en": "A wise person sees all beings as equal.",
        "te": "జ్ఞాని సమస్త ప్రాణులను సమానంగా చూస్తాడు.",
        "hi": "ज्ञानी सभी जीवों को समान रूप में देखता है।"
    },
    {
        "en": "Anger leads to delusion, and delusion leads to loss of memory.",
        "te": "కోపం మోహానికి దారితీస్తుంది, మోహం జ్ఞాపకశక్తిని కోల్పోవడానికి దారితీస్తుంది.",
        "hi": "क्रोध से मोह होता है, मोह से स्मृति का नाश होता है।"
    },
    {
        "en": "Meditation purifies the mind.",
        "te": "ధ్యానం మనసును శుద్ధి చేస్తుంది.",
        "hi": "ध्यान मन को शुद्ध करता है।"
    },
    {
        "en": "The soul is neither born, nor does it die.",
        "te": "ఆత్మ పుట్టదు, చచ్చదు కూడా.",
        "hi": "आत्मा ना जन्म लेती है, ना मरती है।"
    }
]

def get_today_index():
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return day_of_year % len(shlokas)

def get_daily_shloka(language="en"):
    index = get_today_index()
    return shlokas[index].get(language, shlokas[index]["en"])
