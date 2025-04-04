from __future__ import annotations

from typing import TypedDict


class Greeting(TypedDict):
    """A dictionary that contains the greeting phrase 'Hello' in a specified language."""

    country: str
    language: str
    greeting: str
    iso_code: str
    country_in_english: str
    language_in_english: str

# the english phrase "Hello" in different languages / dialects as spoken in a country
greetings: list[Greeting] = [
    {"country": "Deutschland", "language": "deutsch", "greeting": "Hallo",
     "iso_code": "de", "country_in_english": "Germany", "language_in_english": "German"},
    {"country": "Österreich", "language": "deutsch", "greeting": "Servus",
     "iso_code": "at", "country_in_english": "Austria", "language_in_english": "German"},
    {"country": "USA", "language": "English", "greeting": "Hello",
     "iso_code": "us", "country_in_english": "USA", "language_in_english": "English"},
    {"country": "Australia", "language": "English", "greeting": "Hello", "iso_code": "au",
     "country_in_english": "Australia", "language_in_english": "English"},
    {"country": "New Zealand", "language": "English", "greeting": "Hello",
     "iso_code": "nz", "country_in_english": "New Zealand",
     "language_in_english": "English"},
    {"country": "Great Britain", "language": "English", "greeting": "Hello",
     "iso_code": "gb",
     "country_in_english": "Great Britain", "language_in_english": "English"},
    {"country": "Sverige", "language": "svenska", "greeting": "Hallå",
     "iso_code": "se", "country_in_english": "Sweden", "language_in_english": "Swedish"},
    {"country": "Norge", "language": "norsk", "greeting": "Hallo", "iso_code": "no",
     "country_in_english": "Norway", "language_in_english": "Norwegian"},
    {"country": "الأردن", "language": "عربي", "greeting": "مرحبا",
     "iso_code": "jo", "country_in_english": "Jordan", "language_in_english": "Arabic"},
    {"country": "Singapore", "language": "English", "greeting": "Hello",
     "iso_code": "sg", "country_in_english": "Singapore",
     "language_in_english": "English"},
    {"country": "France", "language": "française", "greeting": "Bonjour",
     "iso_code": "fr", "country_in_english": "France", "language_in_english": "French"},
    {"country": "España", "language": "Español", "greeting": "Hola",
     "iso_code": "es", "country_in_english": "Spain", "language_in_english": "Spanish"},
    {"country": "Portugal", "language": "Português", "greeting": "Olá", "iso_code": "pt",
     "country_in_english": "Portugal", "language_in_english": "Portuguese"},
    {"country": "日本", "language": "日本語", "greeting": "こんにちは",
     "iso_code": "jp", "country_in_english": "Japan", "language_in_english": "Japanese"},
    {"country": "Nederland", "language": "Nederlands", "greeting": "Hallo",
     "iso_code": "nl", "country_in_english": "Netherlands",
     "language_in_english": "Dutch"},
    {"country": "België", "language": "Nederlands", "greeting": "Hallo",
     "iso_code": "be", "country_in_english": "Belgium", "language_in_english": "Dutch"},
    {"country": "한국", "language": "한국어", "greeting": "안녕하세요", "iso_code": "kr",
     "country_in_english": "South Korea", "language_in_english": "Korean"},
    {"country": "Україна", "language": "Українська", "greeting": "Привіт",
     "iso_code": "ua", "country_in_english": "Ukraine",
     "language_in_english": "Ukrainian"},
    {"country": "Indonesia", "language": "Bahasa Indonesia", "greeting": "Halo",
     "iso_code": "id", "country_in_english": "Indonesia",
     "language_in_english": "Indonesian"},
    {"country": "Suomi", "language": "suomi", "greeting": "Hei",
     "iso_code": "fi", "country_in_english": "Finland", "language_in_english": "Finnish"},
    {"country": "Lietuva", "language": "lietuvių", "greeting": "Labas", "iso_code": "lt",
     "country_in_english": "Lithuania", "language_in_english": "Lithuanian"},
    {"country": "Ελλάδα", "language": "Ελληνικά", "greeting": "Γεια σας",
     "iso_code": "gr", "country_in_english": "Greece", "language_in_english": "Greek"},
    {"country": "Magyarország", "language": "Magyar", "greeting": "Sziasztok",
     "iso_code": "hu", "country_in_english": "Hungary",
     "language_in_english": "Hungarian"},
    {"country": "Latvija", "language": "Latviešu", "greeting": "Sveiki",
     "iso_code": "lv", "country_in_english": "Latvia", "language_in_english": "Latvian"},
    {"country": "Italia", "language": "Italiano", "greeting": "Ciao",
     "iso_code": "it", "country_in_english": "Italy", "language_in_english": "Italian"},
    {"country": "Hrvatska", "language": "Hrvatski", "greeting": "zdravo",
     "iso_code": "hr", "country_in_english": "Croatia",
     "language_in_english": "Croatian"},
    {"country": "România", "language": "Română", "greeting": "Salut", "iso_code": "ro",
     "country_in_english": "Romania", "language_in_english": "Romanian"},
    {"country": "新加坡", "language": "中文", "greeting": "你好", "iso_code": "sg",
     "country_in_english": "Singapore", "language_in_english": "Mandarin"},
    {"country": "Türkiye", "language": "Türkçe", "greeting": "Merhaba",
     "iso_code": "tr", "country_in_english": "Turkey", "language_in_english": "Turkish"},
    {"country": "Danmark", "language": "Dansk", "greeting": "Hej",
     "iso_code": "dk", "country_in_english": "Denmark", "language_in_english": "Danish"},
]
