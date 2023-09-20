from django.core.management.base import BaseCommand
from defaultPicker.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        default_pickers = {
            "ages": [
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
                "32",
                "33",
                "34",
                "35",
                "36",
                "37",
                "38",
                "39",
                "40",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "47",
                "48",
                "49",
                "50",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "57",
                "58",
                "59",
            ],
            "ethnicity": [
                "American Indian",
                "Black/ African Descent",
                "East Asian",
                "Hispanic / Latino",
                "Middle Eastern",
                "Pacific Islander",
                "South Asian",
                "White / Caucasian",
                "Other",
                "Prefer Not to Say",
            ],
            "ethnicity_fr": [
                "Amérindien",
                "Noir / Afro Descendant",
                "Asie de L'Est",
                "Hispanique / latino",
                "Moyen-Orient",
                "Insulaire du Pacifique",
                "Sud-Asiatique",
                "Blanc / Caucasien",
                "Autre",
                "Je préfère ne rien dire",
            ],
            "family": [
                "Don’t want kids",
                "Want kids ",
                "Open to kids",
                "Have kids",
                "Prefer not to say",
            ],
            "family_fr": [
                "Je ne veux pas d'enfants",
                "Je veux des enfants",
                "Ouvert aux enfants",
                "J'ai des enfants",
                "Je préfère ne rien dire",
            ],
            "heights": [
                "140",
                "143",
                "146",
                "148",
                "151",
                "153",
                "156",
                "158",
                "161",
                "163",
                "166",
                "168",
                "171",
                "173",
                "176",
                "179",
                "181",
                "184",
                "186",
                "189",
                "191",
                "194",
                "196",
                "199",
                "201",
                "204",
                "207",
                "209",
                "212",
                "214",
                "217",
                "219",
                "222",
                "224",
                "227",
                "229",
                "232",
                "234",
                "237",
                "240",
                "242",
                "245",
                "247",
            ],
            "politics": [
                "Liberal",
                "Moderate",
                "Conservative",
                "Other",
                "Prefer Not to Say",
            ],
            "politics_fr": [
                "Libéral",
                "Modéré",
                "Conservateur",
                "Autre",
                "Je préfère ne rien dire",
            ],
            "religious": [
                "Agnostic",
                "Atheist",
                "Buddhist",
                "Catholic",
                "Christian",
                "Hindu",
                "Jewish",
                "Muslim",
                "Spiritual",
                "Other",
                "Prefer Not to Say",
            ],
            "religious_fr": [
                "Agnostique",
                "Athée",
                "Bouddhiste",
                "Catholique",
                "Chrétien",
                "Hindou",
                "Juif",
                "Musulman",
                "Spirituel",
                "Autre",
                "Je préfère ne rien dire",
            ],
            "genders": ["Male", "Female"],
            "genders_fr": ["Masculin", "féminin"],
            "searchGenders": ["Only Men", "Only Women", "Both"],
            "searchGenders_fr": ["Seuls les hommes", "Seules les femmes", "Les deux"],
            "tag": [
                "nature lover",
                "pet friendly",
                "sports fanatic",
                "haute culture",
                "video gamer",
                "gambler",
                "otaku",
                "foodie",
                "early bird",
                "night owl",
                "musician",
                "nerd",
                "book worm",
                "architect",
                "logician",
                "commander",
                "debater",
                "advocate",
                "mediator",
                "protagonist",
                "campaigner",
                "responsible",
                "defender",
                "executive",
                "social butterfly",
                "virtuoso",
                "adventurer",
                "entrepreneur",
                "entertainer",
                "mechanic",
                "nurturer",
                "artist",
                "idealist",
                "scientist",
                "thinker",
                "caregiver",
                "visionary",
                "creative",
                "philosopher",
                "sensitive",
                "compassionate",
                "ambitious",
                "traditional",
                "comedian",
                "leader",
                "traveler",
                "obnoxious",
                "arrogant",
                "impatient",
                "sarcastic",
                "nihilist",
                "hustler",
                "gangster",
                "Vilain",
            ],
            "tag_fr": [
                "amoureux de la nature",
                "pet friendly",
                "fanatique de sport",
                "haute culture",
                "joueur vidéo",
                "joueur",
                "otaku",
                "gourmand",
                "lève-tôt",
                "oiseau de nuit",
                "musicien",
                "nerd",
                "ver de livre",
                "architecte",
                "logicien",
                "commandant",
                "débatteur",
                "avocat",
                "médiateur",
                "protagoniste",
                "militant",
                "responsable",
                "défenseur",
                "exécutif",
                "papillon social",
                "virtuose",
                "aventurier",
                "entrepreneur",
                "artiste",
                "mécanicien",
                "nourricier",
                "artiste",
                "idéaliste",
                "scientifique",
                "penseur",
                "aidant",
                "visionnaire",
                "créatif",
                "philosophe",
                "sensible",
                "compassionné",
                "ambitieux",
                "traditionnel",
                "humoriste",
                "leader",
                "voyageur",
                "odieux",
                "arrogant",
                "impatient",
                "sarcastique",
                "nihiliste",
                "arnaqueur",
                "gangster",
                "Vilain",
            ],
            "zodiacSigns": [
                "Aries",
                "Taurus",
                "Gemini",
                "Cancer",
                "Leo",
                "Virgo",
                "Libra",
                "Scorpio",
                "Sagittarius",
                "Capricorn",
                "Aquarius",
                "Pisces",
            ],
            "zodiacSigns_fr": [
                "Bélier",
                "Taureau",
                "Gémeaux",
                "Cancer",
                "Lion",
                "Vierge",
                "Balance",
                "Scorpion",
                "Sagittaire",
                "Capricorne",
                "Verseau",
                "Poissons",
            ],
            "languages": [
                {"code": "en", "name": "English", "country_code": "US"},
                {"code": "fr", "name": "French", "country_code": "FR"},
                {"code": "nl", "name": "Dutch", "country_code": "NL"},
                {"code": "de", "name": "German", "country_code": "DE"},
                {"code": "sw", "name": "Swahili", "country_code": "TZ"},
                {"code": "it", "name": "Italian", "country_code": "IT"},
                {"code": "ar", "name": "Arabic", "country_code": "SA"},
                {"code": "iw", "name": "Hebrew", "country_code": "IL"},
                {"code": "ja", "name": "Japenese", "country_code": "JP"},
                {"code": "ru", "name": "Russian", "country_code": "RU"},
                {"code": "fa", "name": "Persian", "country_code": "IR"},
                {"code": "es", "name": "Spanish", "country_code": "ES"},
                {"code": "el", "name": "Greek", "country_code": "GR"},
                {"code": "uk", "name": "Ukranian", "country_code": "UA"},
                {"code": "ko", "name": "Korean", "country_code": "KR"},
                {"code": "pl", "name": "Polish", "country_code": "PL"},
                {"code": "vi", "name": "Vietnamese", "country_code": "VN"},
                {"code": "no", "name": "Norwegian.", "country_code": "NO"},
                {"code": "sv", "name": "Swedish", "country_code": "SE"},
                {"code": "hr", "name": "Croatian", "country_code": "HR"},
                {"code": "cs", "name": "Czech", "country_code": "CZ"},
                {"code": "da", "name": "Danish", "country_code": "DK"},
                {"code": "tl", "name": "Filipino", "country_code": "PH"},  # NO language code found with "tl" for Filipino
                {"code": "fi", "name": "Finnish", "country_code": "FI"},
                {"code": "sl", "name": "Slovenian", "country_code": "SI"},
                {"code": "sq", "name": "Albanian", "country_code": "SQ"},
                {"code": "am", "name": "Amharic", "country_code": "ET"},
                {"code": "hy", "name": "Armenian", "country_code": "AM"},
                {"code": "la", "name": "Latin", "country_code": "IT"},  # NO country code found corresponding to latin
                {"code": "lv", "name": "Latvian", "country_code": "LV"},
                {"code": "ln", "name": "Lingala", "country_code": "CD"},  # Verify CG or CD
                {"code": "th", "name": "Thai", "country_code": "TH"},
                {"code": "az", "name": "Azerbijani", "country_code": "AZ"},
                {"code": "eu", "name": "Basque", "country_code": "ES"},
                {"code": "be", "name": "Belarusian", "country_code": "BG"},
                {"code": "bn", "name": "Bengali", "country_code": "BD"},
                {"code": "bs", "name": "Bosnian", "country_code": "BA"},
                {"code": "bg", "name": "Bulgarian", "country_code": "BG"},
                {"code": "km", "name": "Cambodian", "country_code": "KH"},
                {"code": "ca", "name": "Catalan", "country_code": "ES"},
                {"code": "et", "name": "Estonain", "country_code": "EE"},
                {"code": "gl", "name": "Galician", "country_code": "ES"},
                {"code": "ka", "name": "Georgian", "country_code": "GE"},
                {"code": "zh-cn", "name": "Chinese(Simplified)", "country_code": "CN"},
                {"code": "zh-tw", "name": "ChineseTraditional", "country_code": "TW"},
                {"code": "pt-br", "name": "Portuges(Brazil)", "country_code": "BR"},
                {"code": "pt-pt", "name": "Portugese(Portgal)", "country_code": "PT"},
            ],
        }

        for ethnicity_, ethnicity_fr_ in zip(
            default_pickers["ethnicity"], default_pickers["ethnicity_fr"]
        ):
            e = ethnicity.objects.get_or_create(
                ethnicity=ethnicity_,
                ethnicity_fr=ethnicity_fr_,
                defaults={"ethnicity": ethnicity_, "ethnicity_fr": ethnicity_fr_},
            )[0]
            e.save()

        for searchGender_, searchGender_fr_ in zip(
            default_pickers["searchGenders"], default_pickers["searchGenders_fr"]
        ):
            s = searchGender.objects.get_or_create(
                searchGender=searchGender_,
                searchGender_fr=searchGender_fr_,
                defaults={
                    "searchGender": searchGender_,
                    "searchGender_fr": searchGender_fr_,
                },
            )[0]
            s.save()

        for gender_, gender_fr_ in zip(
            default_pickers["genders"], default_pickers["genders_fr"]
        ):
            g = gender.objects.get_or_create(
                gender=gender_,
                gender_fr=gender_fr_,
                defaults={"gender": gender_, "gender_fr": gender_fr_},
            )[0]
            g.save()

        for age_ in default_pickers["ages"]:
            age.objects.get_or_create(age=age_, defaults={"age": age_})

        for family_, family_fr_ in zip(
            default_pickers["family"], default_pickers["family_fr"]
        ):
            f = family.objects.get_or_create(
                familyPlans=family_,
                familyPlans_fr=family_fr_,
                defaults={"familyPlans": family_, "familyPlans_fr": family_fr_},
            )[0]
            f.save()

        for height_ in default_pickers["heights"]:
            height.objects.get_or_create(height=height_, defaults={"height": height_})

        for politics_, politics_fr_ in zip(
            default_pickers["politics"], default_pickers["politics_fr"]
        ):
            p = politics.objects.get_or_create(
                politics=politics_,
                politics_fr=politics_fr_,
                defaults={"politics": politics_, "politics_fr": politics_fr_},
            )[0]
            p.save()

        for religious_, religious_fr_ in zip(
            default_pickers["religious"], default_pickers["religious_fr"]
        ):
            r = religious.objects.get_or_create(
                religious=religious_,
                religious_fr=religious_fr_,
                defaults={"religious": religious_, "religious_fr": religious_fr_},
            )[0]
            r.save()

        for tag_, tag_fr_ in zip(default_pickers["tag"], default_pickers["tag_fr"]):
            t = tags.objects.get_or_create(
                tag=tag_, tag_fr=tag_fr_, defaults={"tag": tag_, "tag_fr": tag_fr_}
            )[0]
            t.save()

        for zodiacSign_, zodiacSign_fr_ in zip(
            default_pickers["zodiacSigns"], default_pickers["zodiacSigns_fr"]
        ):
            z = zodiacSign.objects.get_or_create(
                zodiacSign=zodiacSign_,
                zodiacSign_fr=zodiacSign_fr_,
                defaults={"zodiacSign": zodiacSign_, "zodiacSign_fr": zodiacSign_fr_},
            )[0]
            z.save()

        for language_ in default_pickers["languages"]:
            lang, is_created = Language.objects.get_or_create(
                language=language_["name"],
                language_code=language_["code"],
                defaults={
                    "language": language_["name"],
                    "language_code": language_["code"],
                    "country_code": language_.get("country_code", None),
                },
            )
            if not is_created:
                lang.country_code = language_.get("country_code", None)
            lang.save()
