import asyncio
import logging
import random
import json
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

import os
TOKEN = os.environ.get("TOKEN")
NATIJALAR_FAYL = "natijalar.json"

TESTS = [
    {
        "savol": "O‘zbekiston Respublikasi din ishlari bo‘yicha qo‘mitasi qachon tashkil topgan?",
        "variantlar": [
            "A) O‘zbekiston Respublikasi Prezidentining 1992-yil 17-mart kunidagi «O‘zbekiston Respublikasi Din ishlari bo‘yicha qo‘mitani tashkil etish to‘g‘risida» gi Farmoniga muvofiq tashkil etilgan",
            "B) O‘zbekiston Respublikasi Prezidentining 1991-yil 7-mart kunidagi «O‘zbekiston Respublikasi Din ishlari bo‘yicha qo‘mitani tashkil etish to‘g‘risida» gi Farmoniga muvofiq tashkil etilgan",
            "C) O‘zbekiston Respublikasi Prezidentining 1992-yil 7-mart kunidagi «O‘zbekiston Respublikasi Din ishlari bo‘yicha qo‘mitani tashkil etish to‘g‘risida» gi Farmoniga muvofiq tashkil etilgan",
            "D) O‘zbekiston Respublikasi Prezidentining 1992-yil 27-mart kunidagi «O‘zbekiston Respublikasi Din ishlari bo‘yicha qo‘mitani tashkil etish to‘g‘risida» gi Farmoniga muvofiq tashkil etilgan"
        ],
        "togri": "C"
    },
    {
        "savol": "Ixvanul muslimin yoki al-ixvon al- muslimin (musulmon birodarlari) diniy siyosiy tashkiloti maqsadi bu…",
        "variantlar": [
            "A) Harbiylashgan eksterimistik islomiy tashkilotlar («Katoib Muhammad», «Junud Alloh», «At-takfir val hijra», «Al-tahrir al- islomiy»),»Hizbut tahrir al-islomiy» diniy-siyosiy partiyasi ham shular jumlasiga kiradi",
            "B) Musulmon birodarlarining «Al-ixvon al-muslimin» jurnali 1933 yil chiqa boshladi",
            "C) 1928 yil Misrning Ismoiliya shahrida tuzilgan, asoschisi shayx Hasan al Banno, maqsadi-musulmon o‘lkalarda «islomiy adolat» tamoyillariga asoslangan jamiyat barpo etish",
            "D) Misr, Suriya, Iordaniya, Livand faoliyat ko‘rsatadigan tashkilot"
        ],
        "togri": "C"
    },
    {
        "savol": "Kiberxavfsizlik tushunchasining mohiyatini bilasizmi",
        "variantlar": [
            "A) Kibermakonda shaxs, jamiyat va davlat manfaatlarining tashqi va ichki tahdidlardan himoyalanganlik holati",
            "B) Kibernetika terminini ilk marta yunon faylasufi Platon tilga olgan bo‘lsa, AQShlik N.Viner «Kibernetika» kitobini 1947 yil yozgan",
            "C) Axborotni qabul qilish, saqlash, uni qayta ishlash hamda undan turli jarayonlarni",
            "D) Boshqarishda foydalanish bilan shug‘ullanadigan fan"
        ],
        "togri": "A"
    },
    {
        "savol": "Valiy (avliyo) so‘zi…",
        "variantlar": [
            "A) Shayxlarga berilgan eng oliy unvon",
            "B) O‘rinbosar",
            "C) Qozilar",
            "D) Allohning do‘sti"
        ],
        "togri": "D"
    },
    {
        "savol": "Dalay-Lama so‘zi ma’nosi...",
        "variantlar": [
            "A) tirik xudo",
            "B) ulug‘lama",
            "C) dengizdek ulug‘lama",
            "D) nurlangan daraxt"
        ],
        "togri": "C"
    },
    {
        "savol": "Zardushtiylikning kunlik diniy marosimlari bu...?",
        "variantlar": [
            "A) Uzarin goh (kun botishdan oldin), Aivisrutrim goh (kun botgandan so‘ng)",
            "B) Xavan goh (tongdan peshingacha), Ushaxin goh (yarim kecha)",
            "C) islomning sunniylik va shialik yoʻnalishi ilohiyotida eʼtirof etiladigan aqidalar yoki imon talablari, dindorlar uchun majburiy hisoblangan, shak keltirmasdan, muhokama yuritmasdan eʼtiqod qilinishi lozim boʻlgan diniy talablar",
            "D) Kunlik namoz amali bu goh marosimi, ya‘ni Xavan goh(tongdan peshingacha), Rapitvin goh (peshindan so‘ng) Uzarin goh (kun botishdan oldin), Aivisrutrim goh (kun botgandan so‘ng), Ushaxin goh (yarim kechadan tongacha)"
        ],
        "togri": "D"
    },
    {
        "savol": "Aqida so‘zining ma’nosi…",
        "variantlar": [
            "A) Islomning sunniylik va shialik yoʻnalishi ilohiyotida eʼtirof etiladigan aqidalar yoki imon talablari, dindorlar uchun majburiy hisoblangan, shak keltirmasdan, muhokama yuritmasdan eʼtiqod qilinishi lozim boʻlgan diniy talablar",
            "B) Tavhid (Allohning yagonaligi), Nubuvvat (paygʻambar) ga ishonish, Adl (ilohiy taqdirning adolatligiga ishonish), Maod (oxiratga ishonish)",
            "C) Kunlik namoz amali bu goh marosimi, ya‘ni Xavan goh(tongdan peshingacha), Rapitvin goh (peshindan so‘ng) Uzarin goh (kun botishdan oldin), Aivisrutrim goh (kun botgandan so‘ng), Ushaxin goh (yarim kechadan tongacha)",
            "D) Allohning yagonaligiga, Farishtalarga borligiga, Muqaddas kitoblarga, Paygʻambarlarga, Oxiratga, Taqdirga qayta tirilishiga ishonish"
        ],
        "togri": "A"
    },
    {
        "savol": "Sunniylik Aqidalari",
        "variantlar": [
            "A) Allohning yagonaligiga, Farishtalarga borligiga, Muqaddas kitoblarga, Paygʻambarlarga, Oxiratga, Taqdirga qayta tirilishiga ishonish",
            "B) Allohning yagonaligiga, Farishtalarning borligiga",
            "C) Islomning sunniylik va shialik yoʻnalishi ilohiyotida eʼtirof etiladigan aqidalar yoki imon talablari, dindorlar uchun majburiy hisoblangan, shak keltirmasdan, muhokama yuritmasdan eʼtiqod qilinishi lozim boʻlgan diniy talablar",
            "D) Adl (ilohiy taqdirning adolatligga ishonish), Maod (oxiratga ishonish)"
        ],
        "togri": "A"
    },
    {
        "savol": "Shialik yoʻnalishi ilohiyotida 5 aqida tan olinadi:",
        "variantlar": [
            "A) Farishtalarga borligiga",
            "B) Tavhid (Allohning yagonaligi), Nubuvvat (paygʻambar) ga ishonish, Adl (ilohiy taqdirning adolatligiga ishonish), Maod (oxiratga ishonish)",
            "C) Islomning sunniylik va shialik yoʻnalishi ilohiyotida eʼtirof etiladigan aqidalar yoki imon talablari, dindorlar uchun majburiy hisoblangan, shak keltirmasdan, muhokama yuritmasdan eʼtiqod qilinishi lozim boʻlgan diniy talablar",
            "D) Paygʻambarlarga, Oxiratga, Taqdirga"
        ],
        "togri": "B"
    },
    {
        "savol": "Ilohiyot ……",
        "variantlar": [
            "A) Dinlarni birlashtiruvchilik yani dinlar o‘z ta'limot tizimini vujudga keltirib, unga e'tiqod qiluvchi ta'limot",
            "B) Xudo toʻgʻrisidagi taʼlimot - diniy aqidalar va ular haqidagi ilohiy koʻrsatmalarni oʻz ichiga olgan asosiy diniy taʼlimot",
            "C) Dinlarni birlashtiruvchilik yani dinlar o‘z ta'limot tizimini vujudga keltirib, unga e'tiqod qiluvchi shaxs jamoani shu ta'limot doirasida saqlashga harakat qiladi",
            "D) Allohning yagonaligiga, Farishtalarning borligiga ishonish"
        ],
        "togri": "B"
    },
    {
        "savol": "Dinning funksiyalari….",
        "variantlar": [
            "A) Olamdagi voqea va hodisalarning sabablarini ilohiy, gʻayritabiiy kuch bilan bog‘lab tushuntirish",
            "B) Kompensatorlik",
            "C) Kompensatorlik, integrativ, regulyativ, Kommunikativ va legitimlovchilik",
            "D) Kommunikativ, legitimlovchilik"
        ],
        "togri": "C"
    },
    {
        "savol": "Dinning kompensatorlik funksiyasi",
        "variantlar": [
            "A) Dinlarni birlashtiruvchilik yani dinlar o‘z ta'limot tizimini vujudga keltirish",
            "B) Har qanday o‘z dinidagilar uchun to‘ldiruvchi, ovutuvchi vazifasini bajaradi",
            "C) E'tiqod qiluvchi shaxs jamoani shu ta'limot doirasida saqlashga harakat qiladi",
            "D) Olamdagi voqea va hodisalarning sabablarini ilohiy, gʻayritabiiy kuch bilan bog‘lab tushuntirish"
        ],
        "togri": "B"
    },
    {
        "savol": "Dinning integrativlik funksiyasi ….",
        "variantlar": [
            "A) Urug‘-qabilaviy, milliy, jahon Geografik, xronologik dinlar tizimini vujudga keltirish",
            "B) Dinlarni birlashtiruvchilik yani dinlar o‘z ta'limot tizimini vujudga keltirib, unga e'tiqod qiluvchi shaxs jamoani shu ta'limot doirasida saqlashga harakat qiladi",
            "C) Har qanday o‘z dinidagilar uchun to‘ldiruvchi, ovutuvchi vazifasini bajaradi",
            "D) Islomning sunniylik va shialik yoʻnalishi ilohiyotida eʼtirof etiladigan aqidalar yoki imon talablari, dindorlar uchun majburiy hisoblangan, shak keltirmasdan, muhokama yuritmasdan eʼtiqod qilinishi lozim boʻlgan diniy talablar"
        ],
        "togri": "B"
    },
    {
        "savol": "Diniy dunyoqarash …..",
        "variantlar": [
            "A) Dinlarni birlashtiruvchilik yani dinlar o‘z ta'limot tizimini vujudga keltirib, unga e'tiqod qiluvchi shaxs jamoani shu ta'limot doirasida saqlashga harakat qiladi",
            "B) Olamdagi voqea va hodisalarning sabablarini ilohiy, gʻayritabiiy kuch bilan bog‘lab tushuntiradi",
            "C) Urug‘-qabilaviy, milliy, jahon Geografik, xronologik dinlarni tushuntiradi",
            "D) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik dinlarni tushuntiradi"
        ],
        "togri": "B"
    },
    {
        "savol": "Dinlar paydo bo‘lishining tasniflari...",
        "variantlar": [
            "A) Urug‘-qabilaviy, milliy, jahon Geografik, xronologik dinlar",
            "B) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik",
            "C) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "D) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom"
        ],
        "togri": "A"
    },
    {
        "savol": "Tarixiy-geografik tasnif:",
        "variantlar": [
            "A) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "B) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik",
            "C) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom",
            "D) a) Shri-Lanka, Tibet, Janubi-Sharqiy Osiyo havzasi buddizmi; b) Xitoy dinlari (daosizm, konfutsiychilik, buddizm maktablari); d) Kore"
        ],
        "togri": "B"
    },
    {
        "savol": "Qadimiy Yaqin va O‘rta Sharq dinlari:",
        "variantlar": [
            "A) a) Shri-Lanka, Tibet, Janubi-Sharqiy Osiyo havzasi buddizmi; b) Xitoy dinlari (daosizm, konfutsiychilik, buddizm maktablari); d) Kore",
            "B) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom",
            "C) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "D) a) toltek va atsteklar dinlari; b) inklar dinlari; d) mayyalar dinlari"
        ],
        "togri": "C"
    },
    {
        "savol": "Yaqin va O‘rta Sharqning payg‘ambarli dinlari:",
        "variantlar": [
            "A) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom",
            "B) a) Shri-Lanka, Tibet, Janubi-Sharqiy Osiyo havzasi buddizmi; b) Xitoy dinlari (daosizm, konfutsiychilik, buddizm maktablari); d) Kore",
            "C) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "D) a) vedalar dinlari; b) hinduizm; d) hind buddizmi (teravada, qiluvchilar o‘ziga xos diniy liboslari maxayana)- bilan ham ajralib turadilar e) jaynizm"
        ],
        "togri": "A"
    },
    {
        "savol": "Hindiston dinlari:",
        "variantlar": [
            "A) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "B) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom",
            "C) a) Shri-Lanka, Tibet, Janubi-Sharqiy Osiyo havzasi buddizmi; b) Xitoy dinlari (daosizm, konfutsiychilik, buddizm maktablari); d) Kore",
            "D) a) vedalar dinlari; b) hinduizm; d) hind buddizmi (teravada, qiluvchilar o‘ziga xos diniy liboslari maxayana)- bilan ham ajralib turadilar e) jaynizm"
        ],
        "togri": "D"
    },
    {
        "savol": "Sharqiy va Janubi-Sharqiy Osiyo dinlari: ya va Yaponiya dinlari.",
        "variantlar": [
            "A) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom",
            "B) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik",
            "C) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "D) a) Shri-Lanka, Tibet, Janubi-Sharqiy Osiyo havzasi buddizmi; b) Xitoy dinlari (daosizm, konfutsiychilik, buddizm maktablari); d) Kore"
        ],
        "togri": "D"
    },
    {
        "savol": "Amerika hindulari dinlari:",
        "variantlar": [
            "A) yahudiylik (yahudiy millatiga xos), hinduizm (hindlarga xos), konfutsiychilik (xitoy millatiga xos), sintoizm (yaponlarga xos) kiradi",
            "B) ma’lum millatga xos bo‘lib, boshqa millat vakillari o‘ziga qabul qilmaydigan dinlar",
            "C) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom",
            "D) a) toltek va atsteklar dinlari; b) inklar dinlari; d) mayyalar dinlari"
        ],
        "togri": "D"
    },
    {
        "savol": "Etnik tasnif. urug‘-qabila dinlari -",
        "variantlar": [
            "A) yahudiylik (yahudiy millatiga xos), hinduizm (hindlarga xos), konfutsiychilik (xitoy millatiga xos), sintoizm (yaponlarga xos) kiradi",
            "B) totemistik, animistik tasavvurlarga asoslangan, o‘z urug‘idan chiqqan sehrgar, shomon yoki qabila boshliqlariga sig‘inuvchi dinlar",
            "C) ma’lum millatga xos bo‘lib, boshqa millat vakillari o‘ziga qabul qilmaydigan dinlar",
            "D) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari"
        ],
        "togri": "B"
    },
    {
        "savol": "millat dinlari …..",
        "variantlar": [
            "A) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik",
            "B) a) Shri-Lanka, Tibet, Janubi-Sharqiy Osiyo havzasi buddizmi; b) Xitoy dinlari (daosizm, konfutsiychilik, buddizm maktablari); d) Kore",
            "C) ma’lum millatga xos bo‘lib, boshqa millat vakillari o‘ziga qabul qilmaydigan dinlar",
            "D) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari"
        ],
        "togri": "C"
    },
    {
        "savol": "Milliy dinlar….",
        "variantlar": [
            "A) Yahudiylik (yahudiy millatiga xos), hinduizm (hindlarga xos), konfutsiychilik (xitoy millatiga xos), sintoizm (yaponlarga xos) kiradi",
            "B) Dunyoda eng ko‘p tarqalgan, kishilarning millati va irqidan qat’i nazar unga e’tiqod qilishlari mumkin bolgan dinlar",
            "C) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "D) a) zardushtiylik; b) yahudiylik; d) xristianlik; e) manixeizm; f) islom"
        ],
        "togri": "A"
    },
    {
        "savol": "Jahon dinlari ……",
        "variantlar": [
            "A) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "B) Yahudiylik (yahudiy millatiga xos), hinduizm (hindlarga xos), konfutsiychilik (xitoy millatiga xos), sintoizm (yaponlarga xos) kiradi",
            "C) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik",
            "D) Dunyoda eng ko‘p tarqalgan, kishilarning millati va irqidan qat’i nazar unga e’tiqod qilishlari mumkin bolgan dinlar"
        ],
        "togri": "D"
    },
    {
        "savol": "Jahon dinlariga kiradi…",
        "variantlar": [
            "A) yahudiylik, islom",
            "B) buddizm, xristianlik va islom",
            "C) totemizm, animizm, fetishizm, shomonlik, sehrgarlik",
            "D) shomonlik, sehrgarlik"
        ],
        "togri": "B"
    },
    {
        "savol": "Dinlar ta’limotiga ko‘ra …",
        "variantlar": [
            "A) monoteistik - yakkaxudolik va politeistik - ko‘pxudolik dinlari, Dinlardagi muqaddas manbalar, dindorlarga bo‘linadi",
            "B) dunyoda eng ko‘p tarqalgan, kishilarning millati va irqidan qat’i nazar unga e’tiqod qilishlari mumkin bolgan dinlar",
            "C) yahudiylik (yahudiy millatiga xos), hinduizm (hindlarga xos), konfutsiychilik (xitoy millatiga xos), sintoizm (yaponlarga xos) kiradi",
            "D) buddizm, xristianlik va islom"
        ],
        "togri": "A"
    },
    {
        "savol": "Monoteistik - Yakkaxudolik…",
        "variantlar": [
            "A) hinduizm, konfutsiychilik dinlari",
            "B) yahudiylik, islom",
            "C) genoteizm shomonlik",
            "D) totemizm, animizm, fetishizm, sehrgarlik"
        ],
        "togri": "B"
    },
    {
        "savol": "Politeistik - ko‘pxudolik",
        "variantlar": [
            "A) xristianlik",
            "B) Islom",
            "C) hinduizm, konfutsiychilik dinlari",
            "D) yahudiylik, islom"
        ],
        "togri": "C"
    },
    {
        "savol": "Diniy eʼtiqodlarning evolyutsiyasi:",
        "variantlar": [
            "A) Misr; Shumer; Akkad; g‘arbiy-somiy; islomgacha arablar dinlari",
            "B) totemizm, animizm, fetishizm, shomonlik, sehrgarlik",
            "C) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik",
            "D) poleteizm, genoteizm, monoteizm"
        ],
        "togri": "D"
    },
    {
        "savol": "Dinning ilk shakllari sifatida ….",
        "variantlar": [
            "A) ma’lum millatga xos bo‘lib, boshqa millat vakillari o‘ziga qabul qilmaydigan dinlar",
            "B) totemizm, animizm, fetishizm, shomonlik, sehrgarlik",
            "C) a) Shri-Lanka, Tibet, Janubi-Sharqiy Osiyo havzasi buddizmi; b) Xitoy dinlari (daosizm, konfutsiychilik, buddizm maktablari); d) Kore",
            "D) O‘rta yer dengizi havzasi dinlari: a) grek; b) rim; d) ellinistik"
        ],
        "togri": "B"
    },
    {
        "savol": "Totemizm ….",
        "variantlar": [
            "A) «shomon» so‘zidan olingan bo‘lib, u tunguschada «o‘ta hayajonlangan», «jazavali kishi» degan ma’noni anglatadi",
            "B) lotincha «anima» so‘zidan olingan bo‘lib, «jon», «ruh» degan ma’nolarni anglatadi - inson, tabiat jismlari va hodisalarining ruhi, joni bor deb e’tiqod qilish, ular bilan muloqot qilish, ularga ta’sir o‘tkazish mumkin, degan qarashlar bilan bog‘liq e’tiqod shakllaridan biri",
            "C) diniy tasavvurlarning eng qadimgi shakllaridan biri bo‘lib, hindular tilida «urug‘, kelib chiqish» ma’nolarini beradi",
            "D) yunoncha pylos «koʻp» + yunoncha théos, «Xudo» - «koʻpxudolik» - eʼtiqod tizimi, bir necha xudolarga ishonishga asoslangan diniy dunyoqarash"
        ],
        "togri": "C"
    },
    {
        "savol": "Animizm…..",
        "variantlar": [
            "A) lotincha «anima» so‘zidan olingan bo‘lib, «jon», «ruh» degan ma’nolarni anglatadi - inson, tabiat jismlari va hodisalarining ruhi, joni bor deb e’tiqod qilish, ular bilan muloqot qilish, ularga ta’sir o‘tkazish mumkin, degan qarashlar bilan bog‘liq e’tiqod shakllaridan biri",
            "B) «shomon» so‘zidan olingan bo‘lib, u tunguschada «o‘ta hayajonlangan», «jazavali kishi» degan ma’noni anglatadi",
            "C) yunoncha pylos «koʻp» - yunoncha théos, «Xudo» - «koʻpxudolik» - eʼtiqod tizimi, bir necha xudolarga ishonishga asoslangan diniy dunyoqarash",
            "D) diniy tasavvurlarning eng qadimgi shakllaridan biri bo‘lib, hindular tilida «urug‘, kelib chiqish» ma’nolarini beradi"
        ],
        "togri": "A"
    },
    {
        "savol": "Shomonlik …..",
        "variantlar": [
            "A) inson, tabiat jismlari va hodisalarining ruhi, joni bor deb e’tiqod qilish",
            "B) «shomon» so‘zidan olingan bo‘lib, u tunguschada «o‘ta hayajonlangan», «jazavali kishi» degan ma’noni anglatadi",
            "C) muloqot qilish, ularga ta’sir o‘tkazish mumkin, degan qarashlar bilan bog‘liq e’tiqod shakllaridan biri",
            "D) koʻpxudolikni inkor qilmaydi, biroq ulardan birini tanlab olishni taklif etadi. Unga koʻra tanlab olingan Xudo qolganlaridan ustun degan tushunchani inkor etadi"
        ],
        "togri": "B"
    },
    {
        "savol": "Politeizm ....",
        "variantlar": [
            "A) lotincha «anima» so‘zidan olingan bo‘lib, «jon», «ruh» degan ma’nolarni anglatadi",
            "B) koʻpxudolikni inkor qilmaydi, biroq ulardan birini tanlab olishni taklif etadi. Unga koʻra tanlab olingan Xudo qolganlaridan ustun degan tushunchani inkor etadi",
            "C) «shomon» so‘zidan olingan bo‘lib, u tunguschada «o‘ta hayajonlangan», «jazavali kishi» degan ma’noni anglatadi",
            "D) yunoncha pylos «koʻp» - yunoncha théos, «Xudo» - «koʻpxudolik» - eʼtiqod tizimi, bir necha xudolarga ishonishga asoslangan diniy dunyoqarash"
        ],
        "togri": "D"
    },
    {
        "savol": "Enoteizm yoki genoteizm",
        "variantlar": [
            "A) Enoteizm - koʻpxudolikni inkor qilmaydi, biroq ulardan birini tanlab olishni taklif etadi. Unga koʻra tanlab olingan Xudo qolganlaridan ustun degan tushunchani inkor etadi",
            "B) Etimologik jihatdan bu so‘z yunon tilidan «monos» - «birlik» degan ma'noni anglatadi",
            "C) «Shomon» so‘zidan olingan bo‘lib, u tunguschada «o‘ta hayajonlangan», «jazavali kishi» degan ma’noni anglatadi",
            "D) Din sosiologiyasi bilan shug‘ullanish"
        ],
        "togri": "A"
    },
    {
        "savol": "Monoteizm.",
        "variantlar": [
            "A) Din vazifalarining falsafiy, nazariy jihatlari",
            "B) Enoteizm - koʻpxudolikni inkor qilmaydi, biroq ulardan birini tanlab olishni taklif etadi. Unga koʻra tanlab olingan",
            "C) Etimologik jihatdan bu so‘z yunon tilidan «monos» - «birlik» degan ma'noni anglatadi",
            "D) «Shomon» so‘zidan olingan bo‘lib, u tunguschada «o‘ta hayajonlangan», «jazavali kishi» degan ma’noni anglatadi"
        ],
        "togri": "C"
    },
    {
        "savol": "Din sosiologiyasi nima bilan shug‘ullanadi",
        "variantlar": [
            "A) «dinning o‘zi nima?», «uning mohiyati nimadan iborat?» degan savolga javob beradi",
            "B) legitimlovchilik-qonunlashtiruvchilik vazifasini bajaradi",
            "C) «dinning o‘zi nima?», «uning mohiyati nimadan iborat?» degan savol nuqtai nazaridan yondashishdan tashqari «din qay tarzda faoliyat olib boradi?» degan savol nuqtai nazaridan yondashadi",
            "D) koʻpxudolikni inkor qilmaydi, biroq ulardan birini tanlab olishni taklif etadi. Unga koʻra tanlab olingan Xudo qolganlaridan ustun degan tushunchani inkor etadi"
        ],
        "togri": "C"
    },
    {
        "savol": "Regulyatorlik….. vazifasini bajaradi.",
        "variantlar": [
            "A) aloqa bog‘lashlik, birlashtiruvchilik vazifasini bajaradi",
            "B) «dinning o‘zi nima?», «uning mohiyati nimadan iborat?» degan savolga javob beradi",
            "C) tartibga solib, nazorat qiluvchilik",
            "D) qonunlashtiruvchilik vazifasini bajaradi"
        ],
        "togri": "C"
    },
    {
        "savol": "Integratorlik …. vazifasini bajaradi",
        "variantlar": [
            "A) aloqa bog‘lashlik, birlashtiruvchilik",
            "B) tartibga solib, nazorat qiluvchilik vazifasini bajaradi",
            "C) «dinning o‘zi nima?», «uning mohiyati nimadan iborat?» degan savolga javob beradi",
            "D) din vazifalarining falsafiy, nazariy jihatlarini o‘rganadi"
        ],
        "togri": "A"
    },
    {
        "savol": "Legitimchilik….. vazifasi",
        "variantlar": [
            "A) qonunlashtiruvchilik",
            "B) aloqa bog‘lashlik, birlashtiruvchilik",
            "C) tartibga solib, nazorat qiluvchilik vazifasini bajaradi",
            "D) «dinning o‘zi nima?», «uning mohiyati nimadan iborat?» degan savolga javob beradi"
        ],
        "togri": "A"
    },
    {
        "savol": "Legitimlovchilik-qonunlashtiruvchilik vazifasining asoschisi",
        "variantlar": [
            "A) T.Parsons",
            "B) Gegel",
            "C) Muller",
            "D) Teylor"
        ],
        "togri": "A"
    },
    {
        "savol": "Din vazifalarining falsafiy, nazariy jihatlari",
        "variantlar": [
            "A) Diniy qarashlarni majburan singdirishga yo‘l qo‘yilmaydi»",
            "B) Bu vazifa insonga yashashdan maqsad, hayot mazmunini, dorulfano va dorulbaqo dunyo masalalariga o‘z munosabatini bildirib turishidan iboratdir",
            "C) Din va diniy e’tiqod haqida ilmiy, dunyoviy tasavvur hosil qilishga yordam berish",
            "D) Koʻpxudolikni inkor qilmaydi, biroq ulardan birini tanlab olishni taklif etadi. Unga koʻra tanlab olingan Xudo qolganlaridan ustun degan tushunchani inkor etadi"
        ],
        "togri": "B"
    },
    {
        "savol": "O‘zbekiston Konstitutsiyasida dinning mamlakatimizdagi ijtimoiy o‘rni aniq belgilab qo‘yilgan……",
        "variantlar": [
            "A) 45-modda Har bir inson xohlagan dinga e’tiqod qilish yoki hech qaysi dinga e’tiqod qilmaslik huquqiga ega",
            "B) 31-modda «Hamma uchun vijdon erkinligi kafolatlanadi",
            "C) 35-modda «Hamma uchun vijdon erkinligi kafolatlanadi. Har bir inson xohlagan dinga e’tiqod qilish yoki hech qaysi dinga e’tiqod qilmaslik huquqiga ega. Diniy qarashlarni majburan singdirishga yo‘l qo‘yilmaydi»",
            "D) 55-modda Diniy qarashlarni majburan singdirishga yo‘l qo‘yilmaydi»"
        ],
        "togri": "C"
    },
    {
        "savol": "Dinshunoslik fanining vazifalaridan biri…",
        "variantlar": [
            "A) Diniy qarashlarni majburan singdirishga yo‘l qo‘yilmaslik",
            "B) Falastinda miloddan avvalgi II ming yillikning oxirlari - I ming yillikning boshlarida vujudga kelgan dinlarni urgatish",
            "C) 35-moddani urgatish",
            "D) Din va diniy e’tiqod haqida ilmiy, dunyoviy tasavvur hosil qilishga yordam berish"
        ],
        "togri": "D"
    },
    {
        "savol": "Dinshunoslik fanining vazifalaridan biri…",
        "variantlar": [
            "A) Falastinda miloddan avvalgi II ming yillikning oxirlari - I ming yillikning boshlarida vujudga kelgan dinlarni urgatish",
            "B) Dinning inson hayotida tutgan o‘rni va mavqeyi haqida to‘g‘ri tushunchani shakllantirish",
            "C) 35-moddani urgatish",
            "D) Diniy qarashlarni majburan singdirishga yo‘l qo‘yilmaslik"
        ],
        "togri": "B"
    },
    {
        "savol": "Dinshunoslik fanining vazifalaridan biri…",
        "variantlar": [
            "A) Diniy qarashlarni majburan singdirishga yo‘l qo‘yilmaslik",
            "B) Kishi ma’naviyatida ma’naviy bo‘shliq (vakuum) yuzaga kelishiga yo‘l qo‘ymaslik, turli g‘ayritabiiy va g‘ayriinsoniy diniy qarashlar shakllanishining oldini olish",
            "C) Falastinda miloddan avvalgi II ming yillikning oxirlari - I ming yillikning boshlarida vujudga kelgan dinlarni urgatish",
            "D) diniy e’tiqod qaysi shaklda bo‘lmasin, ezgulik, odamiylik va adolat g‘oyalariga bo‘ysunganligini isbotlashga ko‘maklashadi, dinlar o‘rtasida mazkur g‘oyalar asosida ma’naviy yakdillik va hamjihatlik aloqalari mavjudligini isbotlashga xizmat qiladi"
        ],
        "togri": "B"
    },
    {
        "savol": "Dinshunoslik -",
        "variantlar": [
            "A) aloqa bog‘lashlik, birlashtiruvchilik dinlarini urgatish",
            "B) legitimchilik….. vazifasi va dinlarni urgatish",
            "C) qonunlashtiruvchilik dinlarini urgatish",
            "D) diniy e’tiqod qaysi shaklda bo‘lmasin, ezgulik, odamiylik va adolat g‘oyalariga bo‘ysunganligini isbotlashga ko‘maklashadi, dinlar o‘rtasida mazkur g‘oyalar asosida ma’naviy yakdillik va hamjihatlik aloqalari mavjudligini isbotlashga xizmat qiladi"
        ],
        "togri": "D"
    },
    {
        "savol": "Dinshunoslikning huquqshunoslik bilan bog‘liqligi",
        "variantlar": [
            "A) legitimchilik….. vazifasi va dinlarni urgatish",
            "B) dinning konstitutsiyaviy mavqeyi, huquqqa ta’siri, vijdon erkinligi, so‘z erkinligi kabilarga bog‘liqligi masalalarini o‘rganadi",
            "C) diniy e’tiqod qaysi shaklda bo‘lmasin, ezgulik, odamiylik va adolat g‘oyalariga bo‘ysunganligini isbotlashga ko‘maklashadi, dinlar o‘rtasida mazkur g‘oyalar asosida ma’naviy yakdillik va hamjihatlik aloqalari mavjudligini isbotlashga xizmat qiladi",
            "D) aloqa bog‘lashlik, birlashtiruvchilik dinlarini urgatish"
        ],
        "togri": "B"
    },
    {
        "savol": "Yahudiylik dinining yuzaga kelishi.",
        "variantlar": [
            "A) Falastinda miloddan avvalgi II ming yillikning oxirlari - I ming yillikning boshlarida vujudga kelgan",
            "B) Miloddan avvalgi III ming yillikning oxirlarida vujudga kelgan",
            "C) Falastinda miloddan avvalgi I ming yillikning boshlarida vujudga kelgan",
            "D) Milodiy II ming yillikning boshlarida vujudga kelgan"
        ],
        "togri": "A"
    },
    {
        "savol": "Yahudiylik dinining muqaddas kitobi",
        "variantlar": [
            "A) Avesto",
            "B) Injil",
            "C) Tripitaka",
            "D) Tavrot"
        ],
        "togri": "D"
    },
    {
        "savol": "Tavrot quyidagi kitoblardan iborat:",
        "variantlar": [
            "A) Borliq, Chiqish, Loviy, Sonlar, Ikkinchi qonun",
            "B) Tavrot, Tripitaka",
            "C) Injil, Avesto, Tavrot, Tripitaka",
            "D) Tavrot, Injil"
        ],
        "togri": "A"
    },
    {
        "savol": "Yahudiylik dinining asoschisi",
        "variantlar": [
            "A) Iso payg‘ambar",
            "B) Muso payg‘ambar",
            "C) Dovud payg‘ambar",
            "D) Nuh payg‘ambar"
        ],
        "togri": "B"
    },
    {
        "savol": "Tavrotning «Chiqish» va «Ikkinchi qonun» qismlarida qayd etilgan Ahdnomaning mazmuni …",
        "variantlar": [
            "A) 1) Yaxvega sig‘inish; 2) Yaxvedan boshqa mavjudotlarni ilohiylashtirmaslik, 3) xudoning nomini besabab tilga olmaslik; 4) haftaning olti kunida ishlab, shanba kunida xudoga sig‘inish",
            "B) Barchasi to‘g‘ri",
            "C) 5) ota-onani hurmat qilish; 6) odam o‘ldirmaslik; 7) zino qilmaslik",
            "D) 8) o‘g‘rilik qilmaslik; 9) yaqin kishilarga yolg‘on guvohlik bermaslik; 10) yaqin kishilarning haqiga xiyonat qilmaslik"
        ],
        "togri": "B"
    },
    {
        "savol": "Vedalar",
        "variantlar": [
            "A) «Rigveda» (qasida, madhiya, duolar toʻplami), «Samaveda» (qoʻshiqlar toʻplami), Yajurveda (qurbonlik qilish yoʻllari), Atharvaveda (sehrli duolar toʻplami) yetib kelgan",
            "B) (sanskritcha veda - bilim)- Hindiston yozma adabiyotining qad. yodgorligi. Mil. av. 2-ming yillikning oxiri - 1-ming yillikning boshida yaratilib, Veda toʻplamlari deb nomlanadi",
            "C) 5) ota-onani hurmat qilish; 6) odam o‘ldirmaslik; 7) zino qilmaslik",
            "D) Yajurveda (qurbonlik qilish yoʻllari), Atharvaveda (sehrli duolar toʻplami) yetib kelgan"
        ],
        "togri": "B"
    },
    {
        "savol": "Vedalar….",
        "variantlar": [
            "A) 1) Yaxvega sig‘inish; 2) Yaxvedan boshqa mavjudotlarni ilohiylashtirmaslik, 3) xudoning nomini besabab tilga olmaslik; 4) haftaning olti kunida ishlab, shanba kunida xudoga sig‘inish",
            "B) (sanskritcha veda - bilim)- Hindiston yozma adabiyotining qad. yodgorligi. Mil. av. 2-ming yillikning oxiri - 1-ming yillikning boshida yaratilib, Veda toʻplamlari deb nomlanadi",
            "C) «Rigveda» (qasida, madhiya, duolar toʻplami), «Samaveda» (qoʻshiqlar toʻplami), Yajurveda (qurbonlik qilish yoʻllari), Atharvaveda (sehrli duolar toʻplami) yetib kelgan",
            "D) Qurbonlik qilish yoʻllari"
        ],
        "togri": "C"
    },
    {
        "savol": "Mitra -",
        "variantlar": [
            "A) Qurbonlik qilish tangrisi",
            "B) Ajal, oʻlim keltiruvchi",
            "C) Quyosh tangrisi",
            "D) Osmon xudosi"
        ],
        "togri": "C"
    },
    {
        "savol": "Varuna -",
        "variantlar": [
            "A) Ajal, oʻlim keltiruvchi",
            "B) Quyosh tangrisi",
            "C) Osmon maʼbudi",
            "D) Qurbonlik qilish tangrisi"
        ],
        "togri": "C"
    },
    {
        "savol": "Agni -",
        "variantlar": [
            "A) Olov maʼbudi",
            "B) Oy maʼbudasi",
            "C) Quyosh tangrisi",
            "D) Ajal, oʻlim keltiruvchi"
        ],
        "togri": "A"
    },
    {
        "savol": "Yama -,",
        "variantlar": [
            "A) Quyosh tangrisi",
            "B) Koinot tartibini anglatadi",
            "C) Oy maʼbudasi",
            "D) Ajal, oʻlim keltiruvchi"
        ],
        "togri": "D"
    },
    {
        "savol": "Sama -,",
        "variantlar": [
            "A) Ajal, oʻlim keltiruvchi",
            "B) Oy maʼbudasi",
            "C) Qurbonlik qilish tangrisi",
            "D) Osmon xudosi"
        ],
        "togri": "B"
    },
    {
        "savol": "Rita -",
        "variantlar": [
            "A) Koinot tartibini anglatadi",
            "B) Ajal, oʻlim keltiruvchi",
            "C) Qurbonlik qilish tangrisi",
            "D) Osmon xudosi"
        ],
        "togri": "A"
    },
    {
        "savol": "Yahudiylar jamoasining ibodad joyi…..",
        "variantlar": [
            "A) Sinagoga",
            "B) Masjid",
            "C) Cherkov",
            "D) sangarama"
        ],
        "togri": "A"
    },
    {
        "savol": "Vedalar",
        "variantlar": [
            "A) Qurbonlik qilish yoʻllari",
            "B) Qasida, madhiya, duolar toʻplami",
            "C) Sanskritcha «bilim» - Hindiston yozma adabiyotining qad. yodgorligi",
            "D) Qoʻshiqlar toʻplami"
        ],
        "togri": "C"
    },
    {
        "savol": "«Rigveda»",
        "variantlar": [
            "A) Qasida, madhiya, duolar toʻplami",
            "B) Qurbonlik qilish yoʻllari",
            "C) Qoʻshiqlar toʻplami",
            "D) Sehrli duolar toʻplami"
        ],
        "togri": "A"
    },
    {
        "savol": "«Samaveda»",
        "variantlar": [
            "A) Qoʻshiqlar toʻplami",
            "B) Qasida, madhiya, duolar toʻplami",
            "C) Qurbonlik qilish yoʻllari",
            "D) Sehrli duolar toʻplami"
        ],
        "togri": "A"
    },
    {
        "savol": "Yajurveda",
        "variantlar": [
            "A) Qoʻshiqlar toʻplami,",
            "B) Qurbonlik qilish yoʻllari",
            "C) Qasida, madhiya, duolar toʻplami",
            "D) Sehrli duolar toʻplami"
        ],
        "togri": "B"
    },
    {
        "savol": "Atharvaveda",
        "variantlar": [
            "A) Qasida, madhiya, duolar toʻplami",
            "B) Qurbonlik qilish yoʻllari",
            "C) Qoʻshiqlar toʻplami",
            "D) Sehrli duolar toʻplami"
        ],
        "togri": "D"
    },
    {
        "savol": "Jinna so‘zining mazmuni …",
        "variantlar": [
            "A) Qoʻshiq",
            "B) Qurbonlik",
            "C) Gʻolib",
            "D) Qasida, madhiya"
        ],
        "togri": "C"
    },
    {
        "savol": "Upanishad",
        "variantlar": [
            "A) Maxfiy taʼlimotlarga asoslangan falsafiy-diniy risolalar",
            "B) borliqning ibtidosi va intihosi",
            "C) Asosiy yaratuvchi va o‘z navbatida hech qachon yaratilmagan xudo",
            "D) Brahman, Shiva va Vishnu"
        ],
        "togri": "A"
    },
    {
        "savol": "Brahma -",
        "variantlar": [
            "A) Borliqning ibtidosi va intihosi, barcha mavjudotlarning asosi, deb ulugʻlanadi",
            "B) Maxfiy taʼlimotlarga asoslangan falsafiy-diniy risolalar",
            "C) Jonning yangi shaklga kirishi «sansara« haqidagi taʼlimot yotadi",
            "D) Asosiy yaratuvchi va o‘z navbatida hech qachon yaratilmagan xudo"
        ],
        "togri": "A"
    },
    {
        "savol": "Brahman nima ?",
        "variantlar": [
            "A) Maxfiy taʼlimotlarga asoslangan falsafiy-diniy risolalar",
            "B) Borliqning ibtidosi va intihosi, barcha mavjudotlarning asosi, deb ulugʻlanadi",
            "C) Asosiy yaratuvchi va o‘z navbatida hech qachon yaratilmagan xudo",
            "D) Borliqning ibtidosi va intihosi"
        ],
        "togri": "C"
    },
    {
        "savol": "Hinduizm xudolari",
        "variantlar": [
            "A) Brahman, Shiva va Vishnu",
            "B) Varuna",
            "C) Yaxve",
            "D) Mitra"
        ],
        "togri": "A"
    },
    {
        "savol": "Hinduiylikning asosida …",
        "variantlar": [
            "A) borliqning ibtidosi va intihosi",
            "B) barcha mavjudotlarning asosi, deb ulugʻlanadi",
            "C) maxfiy taʼlimotlarga asoslangan falsafiy-diniy risolalar",
            "D) jonning yangi shaklga kirishi «sansara« haqidagi taʼlimot yotadi"
        ],
        "togri": "D"
    },
    {
        "savol": "Hozirgi Hinduiylikdagi oqimlar",
        "variantlar": [
            "A) pravoslav",
            "B) katolik",
            "C) vishnuizm va shivaizm",
            "D) protestant"
        ],
        "togri": "C"
    },
    {
        "savol": "JAYNIZM qachon paydo boʻlgan",
        "variantlar": [
            "A) VI asrda",
            "B) Mil. av. V asrda",
            "C) Mil. av. I asrda",
            "D) Mil. av. VI asrda"
        ],
        "togri": "D"
    },
    {
        "savol": "Jaynizmda markaziy taʼlimot nima?",
        "variantlar": [
            "A) jon haqidagi taʼlimot",
            "B) insonparvarlik (jen)",
            "C) odob qoidalari (li)",
            "D) fazilat (de) tushunchalari"
        ],
        "togri": "A"
    },
    {
        "savol": "Sikxiylikning muqaddas kitobi -",
        "variantlar": [
            "A) Adigrantx («Boshlang‘ich kitob») bo‘lib, beshinchi guru Arjun (1581-1606) tomonidan tuzilgan. U, shuningdek, Gururantx («Guru kitobi») yoki Grantxsahib («Sohibning kitobi») nomlari bilan ham ataladi",
            "B) Borliq, Chiqish, Loviy, Sonlar, Ikkinchi qonun",
            "C) Tavrot, Tripitaka",
            "D) Injil, Avesto, Tavrot, Tripitaka"
        ],
        "togri": "A"
    },
    {
        "savol": "Konfutsiy taʼlimotida nima muhim oʻrin egallaydi.",
        "variantlar": [
            "A) Borliq",
            "B) Insonparvarlik (jen), odob qoidalari (li), fazilat (de) tushunchalari",
            "C) Chiqish",
            "D) Loviy, Sonlar, Ikkinchi qonun"
        ],
        "togri": "B"
    },
    {
        "savol": "Daosizm qachon, qaerda vujudga kelgan. Asoschisi kim?",
        "variantlar": [
            "A) Miloddan avvalgi V-asrda vujudga kelgan",
            "B) Miloddan avvalgi VI-V-asrlarda vujudga kelgan. Asoschisi Lao-szi hisoblanadi",
            "C) Miloddan avvalgi VI asrda vujudga kelgan",
            "D) Miloddan avvalgi VII-asrda vujudga kelgan"
        ],
        "togri": "B"
    },
    {
        "savol": "Daosizmning gʻoyalari qaysi kitobda bayon etilgan",
        "variantlar": [
            "A) Chiqish",
            "B) Borliq",
            "C) «Dao de szin»",
            "D) Loviy, Sonlar, Ikkinchi qonun"
        ],
        "togri": "C"
    },
    {
        "savol": "Sintoizm -",
        "variantlar": [
            "A) Ya’ni «Eng yaxshi din» deb ulug‘langan",
            "B) Sintoizmdagi Oliy Xudo nomi",
            "C) Yaponcha shinto, aynan - Xudolar yoʻli, Xudolar taʼlimoti degan ma’noni bildirib, VI-VII-asrlarda vujudga kelgan Yaponiyada tarqalgan",
            "D) Zoroastr, pahlaviycha- Zaraxustra «boqiy yulduz» va «chiroyli tuyalarga ega bo‘lgan»"
        ],
        "togri": "C"
    },
    {
        "savol": "Sintoizmdagi Oliy Xudo nomi -",
        "variantlar": [
            "A) Amaterasu (quyosh Homiysi)",
            "B) ya’ni «Eng yaxshi din» deb ulug‘langan",
            "C) Zoroastr, pahlaviycha- Zaraxustra «boqiy yulduz» va",
            "D) «chiroyli tuyalarga ega bo‘lgan»"
        ],
        "togri": "A"
    },
    {
        "savol": "Zaratushtra -",
        "variantlar": [
            "A) Yunoncha - Zoroastr, pahlaviycha- Zaraxustra «boqiy yulduz» va «chiroyli tuyalarga ega bo‘lgan»",
            "B) Amaterasu (quyosh Homiysi)",
            "C) Ya’ni «Eng yaxshi din» deb ulug‘langan",
            "D) Sintoizmdagi Oliy Xudo nomi"
        ],
        "togri": "A"
    },
    {
        "savol": "Avestoning axloqiy-falsafiy mohiyati",
        "variantlar": [
            "A) «Ezgu fikr», «ezgu soʻz» va «ezgu amal»",
            "B) «Dao de szin»",
            "C) Borliq",
            "D) Chiqish"
        ],
        "togri": "A"
    },
    {
        "savol": "Zardushtiylikning muqaddas kitobi",
        "variantlar": [
            "A) Avesto",
            "B) «Dao de szin»",
            "C) Borliq",
            "D) Chiqish"
        ],
        "togri": "A"
    },
    {
        "savol": "Zardushtiylikning ehtiromga sazovor xudolari",
        "variantlar": [
            "A) Siddxartxa Gautama, Shakyamuni",
            "B) Ahriman",
            "C) «Mazda»",
            "D) Ahuramazda, Mitra va Anaxita"
        ],
        "togri": "D"
    },
    {
        "savol": "Zardushtiylikning yovuzlik va o‘lim xudosi",
        "variantlar": [
            "A) Ahriman",
            "B) Gautama",
            "C) Shakyamuni",
            "D) Siddxartxa"
        ],
        "togri": "A"
    },
    {
        "savol": "«Avesto» oromiy va pahlaviy yozuvlari asosida yaratilgan -",
        "variantlar": [
            "A) Markaziy Osiyo va Eron xalqlari tarixining qadimgi noyob yodgorligidir",
            "B) «Diniy marosimlar»",
            "C) Yasht ma`no jihatdan Yasnaga yaqin",
            "D) «Barcha ilohlar haqidagi kitob»"
        ],
        "togri": "A"
    },
    {
        "savol": "«Avesto» nechta kitobdan iborat:",
        "variantlar": [
            "A) «Yovuz ruhlarga qarshi qonunlar majmuasi»dan",
            "B) Yasna («Diniy marosimlar»), Yasht (ma`no jihatdan Yasnaga yaqin), Visparad («Barcha ilohlar haqidagi kitob»), Vendidad («Yovuz ruhlarga qarshi qonunlar majmuasi»)",
            "C) «Diniy marosimlar»",
            "D) Yasht ma`no jihatdan Yasnaga yaqin"
        ],
        "togri": "B"
    },
    {
        "savol": "«Mazda» so‘zining ma’nosi",
        "variantlar": [
            "A) Sintoizmdagi Oliy Xudo nomi",
            "B) Ahriman",
            "C) Ya’ni «Eng yaxshi « deb ulug‘langan",
            "D) «Donish, donishmand, oqil»"
        ],
        "togri": "D"
    },
    {
        "savol": "«Mazda» so‘zi oldiga ulug‘lash ma’nosini anglatuvchi «Axura» so‘zi qo‘shilganda ....",
        "variantlar": [
            "A) Ahriman",
            "B) Zardushtiylikning ilohi - «Axura-Mazda» Bu - «Janob Mazda» yoki «Iloh» demakdir",
            "C) Ya’ni «Eng yaxshi « deb ulug‘langan",
            "D) Sintoizmdagi Oliy Xudo nomi"
        ],
        "togri": "B"
    },
    {
        "savol": "Zardushtiylik ta’limotiga ko‘ra,....",
        "variantlar": [
            "A) Dunyo sinovlardan emas, balki yovuzlikka qarshi kurashdan iborat",
            "B) Yovuz ruhlarga qarshi qonunlar",
            "C) Suv, olov, tuproq, havo g`oyat ulug`langan",
            "D) Nurlangan"
        ],
        "togri": "A"
    },
    {
        "savol": "Avestoda to`rt element ….",
        "variantlar": [
            "A) azob-uqubat mavjud; azob-uqubatning sababi (istak) mavjud; azob-uqubatning tugashi (nirvana) mavjud; azob-uqubatning tugashiga olib keluvchi sakkiz bosqichli yoʻl mavjud",
            "B) hayot charxpalagi, uzluksiz qayta tug‘ilishlar tizimi xaqidagi ta’limot",
            "C) yovuz ruhlarga qarshi qonunlar",
            "D) suv, olov, tuproq, havo g`oyat ulug`langan"
        ],
        "togri": "D"
    },
    {
        "savol": "Buddaviylikning muqaddas manbasi",
        "variantlar": [
            "A) Borliq",
            "B) Avesto",
            "C) «Dao de szin»",
            "D) Tripitaka"
        ],
        "togri": "D"
    },
    {
        "savol": "Buddaviylikning asoschisi",
        "variantlar": [
            "A) Marko",
            "B) Matvey",
            "C) Siddxartxa Gautama, Shakyamuni",
            "D) Luka, Ioann"
        ],
        "togri": "C"
    },
    {
        "savol": "Budda so‘zining ma’nosi",
        "variantlar": [
            "A) donish",
            "B) donishmand, oqil",
            "C) nurlangan Budda",
            "D) eng yaxshi"
        ],
        "togri": "C"
    },
    {
        "savol": "Buddizm - bu",
        "variantlar": [
            "A) hayot rohat-farog‘atlaridan butunlay voz kechish yo‘li bilan erishiladigan mutlaq osudalik holati",
            "B) hayot charxpalagi, uzluksiz qayta tug‘ilishlar tizimi xaqidagi ta’limot",
            "C) azob-uqubatning sababi (istak) mavjud",
            "D) azob-uqubatning tugashi (nirvana) mavjud"
        ],
        "togri": "B"
    },
    {
        "savol": "Nirvana -",
        "variantlar": [
            "A) buddizm ta’limotiga ko‘ra, hayot rohat-farog‘atlaridan butunlay voz kechish yo‘li bilan erishiladigan mutlaq osudalik holati",
            "B) azob-uqubatning tugashiga olib keluvchi sakkiz bosqichli yoʻl mavjud",
            "C) azob-uqubat mavjud; azob-uqubatning sababi (istak) mavjud; azob-uqubatning tugashi (nirvana) mavjud; azob-uqubatning tugashiga olib keluvchi sakkiz bosqichli yoʻl mavjud",
            "D) azob-uqubatning tugashi mavjud"
        ],
        "togri": "A"
    },
    {
        "savol": "Buddizm oqimlari",
        "variantlar": [
            "A) shialik",
            "B) Katolik",
            "C) Provoslav",
            "D) xinayana va maxayana"
        ],
        "togri": "D"
    },
    {
        "savol": "Dharma - Gautama qoldirgan «toʻrt oliy haqiqat»",
        "variantlar": [
            "A) «Duolar kitobi» yoʻl mavjud",
            "B) «Axloqiy me’yorlar yoʻl mavjud",
            "C) azob-uqubat mavjud; azob-uqubatning sababi (istak) mavjud; azob-uqubatning tugashi (nirvana) mavjud; azob-uqubatning tugashiga olib keluvchi sakkiz bosqichli yoʻl mavjud",
            "D) yapon tilidan - «tafakkur» degan ma’noni bildirib yoʻl mavjud"
        ],
        "togri": "C"
    },
    {
        "savol": "«Tripitaka»",
        "variantlar": [
            "A) yapon tilidan - «tafakkur» degan ma’noni bildiradi",
            "B) ikki savat donolik»",
            "C) «Duolar kitobi» yoʻl mavjud",
            "D) sanskritcha - «Uch savat donolik»"
        ],
        "togri": "D"
    },
    {
        "savol": "«Vinaya-pitaka»",
        "variantlar": [
            "A) «Diniy-falsafiy masalalar kitobi»",
            "B) sanskritcha - «Axloqiy me’yorlar kitobi»",
            "C) «Uch savat donolik»",
            "D) ikki savat donolik»"
        ],
        "togri": "B"
    },
    {
        "savol": "«Sutta-pitaka»",
        "variantlar": [
            "A) «Uch savat donolik»",
            "B) «Diniy-falsafiy masalalar kitobi»",
            "C) sanskritcha - «Duolar kitobi»",
            "D) ikki savat donolik»"
        ],
        "togri": "C"
    },
    {
        "savol": "«Abxidxarma-pitaka»",
        "variantlar": [
            "A) ikki savat donolik»",
            "B) «Uch savat donolik»",
            "C) sanskritcha - «Diniy-falsafiy masalalar kitobi»",
            "D) yapon tilidan - «tafakkur»"
        ],
        "togri": "C"
    },
    {
        "savol": "Dzen buddaviylik ta'limoti .....",
        "variantlar": [
            "A) ikki savat donolik»",
            "B) «Diniy-falsafiy masalalar kitobi»",
            "C) «Uch savat donolik»",
            "D) yapon tilidan - «tafakkur» degan ma’noni bildirib, Xitoy va butun Sharqiy Osiyo buddizmining eng muhim maktablaridan biri"
        ],
        "togri": "D"
    },
    {
        "savol": "Chan buddizmi Xitoycha «chan», sanskritcha «dhyana» atamasidan kelib chiqqan bo‘lib...",
        "variantlar": [
            "A) ikki savat donolik»",
            "B) sanskritcha - falsafiy masalalar kitobi»",
            "C) savat donolik»",
            "D) «ajralish» yoki «najot» degan ma'noni anglatadi"
        ],
        "togri": "D"
    },
    {
        "savol": "Dalay Lama …",
        "variantlar": [
            "A) Fayoztepa buddist rohiblari",
            "B) Tibet buddist rohiblarining eng oliy ruhiy rahbaridir",
            "C) Qoratepa buddist rohiblari",
            "D) Dalvarzintepa, Ayritom buddist rohiblari"
        ],
        "togri": "B"
    },
    {
        "savol": "O‘zbekistonda buddaviylik dinining tarixiy ildizlari,",
        "variantlar": [
            "A) Suv, olov, tuproq, havo g`oyat ulug`langan",
            "B) Dunyo sinovlardan emas, balki yovuzlikka qarshi kurash",
            "C) Yovuz ruhlarga qarshi qonunlar",
            "D) Qoratepa, Fayoztepa, Dalvarzintepa, Ayritom, Termiz"
        ],
        "togri": "D"
    },
    {
        "savol": "Buddizm monastirlari…",
        "variantlar": [
            "A) Sinagoga",
            "B) Masjid",
            "C) Cherkov",
            "D) Sangarama"
        ],
        "togri": "D"
    },
    {
        "savol": "Xristianlik qachon qaerda vujudga keldi",
        "variantlar": [
            "A) Eramizning boshida Rim imperiyasining g‘arqiy qismida yerlarida",
            "B) Rimning g‘arqiy qismida",
            "C) Eramizning boshida Rim imperiyasining Sharqiy qismida Falastin yerlarida",
            "D) Falastin g‘arqiy qismida"
        ],
        "togri": "C"
    },
    {
        "savol": "Xristianlikning asoschisi",
        "variantlar": [
            "A) Iso Masih",
            "B) Muso",
            "C) Ibrohim",
            "D) Yoqub"
        ],
        "togri": "A"
    },
    {
        "savol": "Iso Masihning onasi",
        "variantlar": [
            "A) Maryam",
            "B) Omina",
            "C) Xadicha",
            "D) Oysha"
        ],
        "togri": "A"
    },
    {
        "savol": "«Masih» so‘zi qadimiy yahudiy tili - ivritdagi «moshiax» Grekchada «xristos» so‘zidan olingan bo‘lib,",
        "variantlar": [
            "A) o‘g‘il-xudo to‘g‘risidagi ta’limot",
            "B) ota-xudo, to‘g‘risidagi ta’limot",
            "C) «Silangan» yoki «Siylangan» ma’nolarini beradi",
            "D) muqaddas ruh - xudo to‘g‘risidagi ta’limot"
        ],
        "togri": "C"
    },
    {
        "savol": "Xristianlik ta’limoti….",
        "variantlar": [
            "A) «Silangan» yoki «Siylangan» ma’nolarini beradi.",
            "B) ota-xudo, o‘g‘il-xudo va muqaddas ruh - uch yuzlik xudo to‘g‘risidagi ta’limot",
            "C) ota-xudo, to‘g‘risidagi ta’limot",
            "D) o‘g‘il-xudo to‘g‘risidagi ta’limot"
        ],
        "togri": "B"
    },
    {
        "savol": "Xristianlikdagi asosiy oqimlar",
        "variantlar": [
            "A) Shialik",
            "B) Pravoslav, Katolik va protestant",
            "C) Forsiylar",
            "D) Saduqiylar"
        ],
        "togri": "B"
    },
    {
        "savol": "Protestant oqimi doirasidagi cherkovlar",
        "variantlar": [
            "A) Forsiylar",
            "B) Pravoslav, Katolik",
            "C) Lyuteranlik, baptizm, anglikanlik va kalvinizm",
            "D) Saduqiylar"
        ],
        "togri": "C"
    },
    {
        "savol": "Xristianlikning muqaddas kitobi",
        "variantlar": [
            "A) Sunan",
            "B) «Sahih»",
            "C) «Injil», «Xushxabar»",
            "D) Avesto"
        ],
        "togri": "C"
    },
    {
        "savol": "Xristianlikning ta’limoti",
        "variantlar": [
            "A) «Silangan» yoki «Siylangan» to‘g‘risidagi ta’limot",
            "B) Ikki mohiyat - odam va xudo mohiyati haqidagi «gunohni yuvish», ya’ni Isoning o‘zini ixtiyoriy tarzda qurbon qilishi haqiqatda",
            "C) Ota-xudo, to‘g‘risidagi ta’limot",
            "D) O‘g‘il-xudo to‘g‘risidagi ta’limot"
        ],
        "togri": "B"
    },
    {
        "savol": "Konstantinopolda II Butun Olam Xristian Sobori qachon bo‘lib o‘tdi",
        "variantlar": [
            "A) 400-yilida",
            "B) 801-yilida",
            "C) 381-yilida",
            "D) 300-yilida"
        ],
        "togri": "C"
    },
    {
        "savol": "Cho‘qintirish sirli hodisasi bu -",
        "variantlar": [
            "A) «silangan» ruhiy tug‘ilishni kasb etadi",
            "B) dindor o‘z tanasini uch marta suvga botirishi Xudo-otani, O‘g‘ilni va Muqaddas ruhni chaqirish bilan ruhiy tug‘ilishni kasb etadi",
            "C) ota-xudo, ruhiy tug‘ilishni kasb etadi",
            "D) o‘g‘il-xudo ruhiy tug‘ilishni kasb etadi"
        ],
        "togri": "B"
    },
    {
        "savol": "Pasxa -",
        "variantlar": [
            "A) Muqaddas kitob va Muqaddas yozuvlar nishonlab o‘tkaziladigan bayram",
            "B) aApostol Pyotr bayrami",
            "C) Isoning o‘lganidan so‘ng qayta tirilganini nishonlab o‘tkaziladigan bayram",
            "D) Martin Lyuter bayrami"
        ],
        "togri": "C"
    },
    {
        "savol": "Katolik oqimining birinchi Yyepiskopi",
        "variantlar": [
            "A) Jan Kalvin",
            "B) Martin Lyuter",
            "C) Apostol Pyotr",
            "D) Vilyam Miller"
        ],
        "togri": "C"
    },
    {
        "savol": "Katolik diniy ta’limotning asosini",
        "variantlar": [
            "A) Muqaddas kitob va Muqaddas yozuvlar tashkil qiladi",
            "B) Yozuvlar",
            "C) Martin Lyuter g‘oyasi",
            "D) Jan Kalvin g‘oyasi"
        ],
        "togri": "A"
    },
    {
        "savol": "Nikohsizlik (selebat) Papa Grigoriy VII tomonidan joriy qilingan qoidaga ko‘ra barcha ruhoniylar uchun majburiydir",
        "variantlar": [
            "A) Protestant",
            "B) Katoliklarda",
            "C) Presviterianlik",
            "D) Baptizm"
        ],
        "togri": "B"
    },
    {
        "savol": "Protestant cherkovining asosiy qoidalarini …….. ishlab chiqdi",
        "variantlar": [
            "A) Jan Kalvin",
            "B) Martin Lyuter",
            "C) Pyotr",
            "D) Vilyam Miller"
        ],
        "togri": "B"
    },
    {
        "savol": "«Tavba qiling, chunki samoviy shohlik yaqinlashib qoldi»",
        "variantlar": [
            "A) «Umumiy ibodatlar kitobi»da",
            "B) M.Lyuterning 95 tezisidan",
            "C) «Suvga cho‘ktirish»",
            "D) Yettinchi kun adventistlari»"
        ],
        "togri": "B"
    },
    {
        "savol": "«Xristian dinidagi ko‘rsatmalar» asari kimga tegishli",
        "variantlar": [
            "A) Jan Kalvin",
            "B) Pyotr",
            "C) Vilyam Miller",
            "D) Martin Lyuter"
        ],
        "togri": "A"
    },
    {
        "savol": "Presviterianlik yunoncha ……",
        "variantlar": [
            "A) «Eng eski» mo‘tadil",
            "B) «Umumiy ibodatlar",
            "C) «Suvga cho‘ktirish»",
            "D) Yettinchi kun"
        ],
        "togri": "A"
    },
    {
        "savol": "Anglikan diniy ta’limoti…. aks ettirilgan",
        "variantlar": [
            "A) baptistlar va zabur xristianlarining asosiy qoidasi",
            "B) «umumiy ibodatlar kitobi»da",
            "C) zabur xristianlarining asosiy qoidasi",
            "D) xristianlarining asosiy qoidasi"
        ],
        "togri": "B"
    },
    {
        "savol": "Baptizm yunoncha …..",
        "variantlar": [
            "A) «suvga cho‘ktirish»",
            "B) «eng eski» mo‘tadil",
            "C) «umumiy ibodatlar",
            "D) yettinchi kun"
        ],
        "togri": "A"
    },
    {
        "savol": "«Hech kim, jumladan, ota-onalar ham kishi uchun biror dinni tanlay olmaydi. Kishi dinni ongli ravishda o‘zi ixtiyor qilmog‘i zarur»….",
        "variantlar": [
            "A) zabur xristianlarining asosiy qoidasi",
            "B) baptistlar va zabur xristianlarining asosiy qoidasi",
            "C) xristianlarining asosiy qoidasi",
            "D) «Umumiy ibodatlar kitobi»da"
        ],
        "togri": "B"
    },
    {
        "savol": "Adventistlar harakatining asoschisi",
        "variantlar": [
            "A) Pyotr",
            "B) Jan Kalvin",
            "C) Vilyam Miller",
            "D) Martin Lyuter"
        ],
        "togri": "C"
    },
    {
        "savol": "Adventistlar bir necha mustaqil cherkovlarga bo‘lingan bo‘lib, ularning eng kattasi",
        "variantlar": [
            "A) «Borliq» yoki «Ibtido»",
            "B) «Yettinchi kun adventistlari»",
            "C) «Chiqish»",
            "D) «Levit»"
        ],
        "togri": "B"
    },
    {
        "savol": "Biblia -",
        "variantlar": [
            "A) kitob, o‘ram ma’nolarini anglatadi",
            "B) «Tora»",
            "C) Netiim (Nabiiyum)",
            "D) («Tavrot»);"
        ],
        "togri": "A"
    },
    {
        "savol": "«Musoning besh kitobi»",
        "variantlar": [
            "A) Marko Injili",
            "B) Netiim (Nabiiyum)",
            "C) Matvey Injili",
            "D) «Tora» («Tavrot»)"
        ],
        "togri": "D"
    },
    {
        "savol": "«Tavrot» quyidagi kitoblarga bo‘linadi:",
        "variantlar": [
            "A) 1) «Borliq» yoki «Ibtido»; 2) «Tora»; 3) «Levit»",
            "B) 1) «Borliq» yoki «Ibtido»; 2) «Chiqish»; 3) «Levit»; 4) «Sonlar»; 5)»Ikkinchi qonun»",
            "C) 1) Netiim (Nabiiyum) 2) «Tora»; 3) «Levit»",
            "D) 1) Netiim (Nabiiyum); 2) «Tora»; 3) «Sonlar»; 4)»Ikkinchi qonun»"
        ],
        "togri": "B"
    },
    {
        "savol": "«Yangi ahd» tarkibiga kirgan Injil nechta kitobga bo‘linadi",
        "variantlar": [
            "A) Matvey",
            "B) 1) Matvey 2) Marko 3) Luka 4) Ioann",
            "C) Marko",
            "D) Luka"
        ],
        "togri": "B"
    },
    {
        "savol": "«Islom» so‘zi arabchadan",
        "variantlar": [
            "A) «Ibodat» deyiladi",
            "B) «Muslim» deyiladi",
            "C) «Muslimun» deyiladi",
            "D) «xudoga o‘zini topshirish», «Itoat», «Bo‘ysunish» ma’nosini beradi"
        ],
        "togri": "D"
    },
    {
        "savol": "Islom diniga ishonuvchilar",
        "variantlar": [
            "A) «Ibodat» deb ataladi",
            "B) Matveyga ishonuvchilar",
            "C) «Muslim» deb ataladi",
            "D) Markoga ishonuvchilar"
        ],
        "togri": "C"
    },
    {
        "savol": "Islom diniga ishonuvchilarning kopchiligi",
        "variantlar": [
            "A) Yahudiylar",
            "B) Xristianlar",
            "C) «Muslimun»",
            "D) buddistlar"
        ],
        "togri": "C"
    },
    {
        "savol": "Muhammad S.A.V.",
        "variantlar": [
            "A) 570 yilda Makkada quraysh qabilasiga mansub bo‘lgan Hoshimiylar xonadonida tug‘ilgan",
            "B) 670 yilda Makkada quraysh qabilasiga mansub bo‘lgan Hoshimiylar xonadonida tug‘ilgan",
            "C) 575 yilda Makkada quraysh qabilasiga mansub bo‘lgan Hoshimiylar xonadonida tug‘ilgan",
            "D) 770 yilda Makkada quraysh qabilasiga mansub bo‘lgan Hoshimiylar xonadonida tug‘ilgan"
        ],
        "togri": "A"
    },
    {
        "savol": "Muhammadga, 40 yoshida",
        "variantlar": [
            "A) milodiy 510-yil vahiy (ilohiy koʻrsatma) kelishni boshladi",
            "B) milodiy 610-yil vahiy (ilohiy koʻrsatma) kelishni boshladi",
            "C) milodiy 410-yil vahiy (ilohiy koʻrsatma) kelishni boshladi",
            "D) milodiy 310-yil vahiy (ilohiy koʻrsatma) kelishni boshladi"
        ],
        "togri": "B"
    },
    {
        "savol": "Madinada Islomni qabul qilganlar",
        "variantlar": [
            "A) ansorlar",
            "B) muhojirlar",
            "C) xorijiylar",
            "D) shialar"
        ],
        "togri": "A"
    },
    {
        "savol": "Madina va Makka oʻrtasida boshlangan kurash……..",
        "variantlar": [
            "A) 8 yil davom etdi. 630-yilda musulmonlar qoʻshini hech qanday qarshiliksiz Makkaga kirib bordi",
            "B) 9 yil davom etdi. 630-yilda musulmonlar qoʻshini hech qanday qarshiliksiz Makkaga kirib bordi",
            "C) 10 yil davom etdi. 630-yilda musulmonlar qoʻshini hech qanday qarshiliksiz Makkaga kirib bordi",
            "D) 8 yil davom etdi. 620-yilda musulmonlar qoʻshini hech qanday qarshiliksiz Makkaga kirib bordi"
        ],
        "togri": "A"
    },
    {
        "savol": "Muhammadning vafoti",
        "variantlar": [
            "A) 630-yilda",
            "B) 632-yilda",
            "C) 532-yilda",
            "D) 635-yilda"
        ],
        "togri": "B"
    },
    {
        "savol": "Muhammad vafotidan soʻng,",
        "variantlar": [
            "A) Abu Bakr Siddiq, Umar ibn Xattob, Usmon ibn Affon va Ali ibn Abu Tolib xalifa sifatida hukmronlik qildilar",
            "B) Umar ibn Xattob, Usmon ibn Affon va Ali ibn Abu Tolib xalifa sifatida hukmronlik qildilar",
            "C) Usmon ibn Affon va Ali ibn Abu Tolib xalifa sifatida hukmronlik qildilar",
            "D) Ali ibn Abu Tolib xalifa sifatida hukmronlik qildi"
        ],
        "togri": "A"
    },
    {
        "savol": "Tavhid arabcha -",
        "variantlar": [
            "A) budda haqidagi taʼlimot",
            "B) ko‘pxudolik - umumiy maʼnoda - ko‘pxudolik haqidagi taʼlimot",
            "C) yakkaxudolik - umumiy maʼnoda - yakkaxudolik haqidagi taʼlimot",
            "D) yahudiylik haqidagi taʼlimot"
        ],
        "togri": "C"
    },
    {
        "savol": "Islom dini 5 «asos» yoki «ustun» (arkon ad-din al-islomiy)ga ega:",
        "variantlar": [
            "A) 1) Kalimai shahodat; 2) Roʻza tutish; 3) Zakot berish; 4) imkoniyat topilsa haj qilish",
            "B) 1) Kalimai shahodat; 2) Namoz oʻqish; 3) Roʻza tutish",
            "C) 1) Kalimai shahodat; 2) Namoz oʻqish; 3) Roʻza tutish; 4) Zakot berish",
            "D) 1) Kalimai shahodat; 2) Namoz oʻqish; 3) Roʻza tutish; 4) Zakot berish; 5) imkoniyat topilsa haj qilish"
        ],
        "togri": "D"
    },
    {
        "savol": "Islomning birinchi ustuni",
        "variantlar": [
            "A) Shahodatdir, yaʼni «Allohdan o‘zga iloh yo‘q» va «Muhammad Allohning rasulidir»",
            "B) zakot",
            "C) Savm yoki roʻzadir",
            "D) haj yoki ziyorat"
        ],
        "togri": "A"
    },
    {
        "savol": "Islomning ikkinchi ustuni",
        "variantlar": [
            "A) savm yoki roʻzadir",
            "B) zakot",
            "C) namoz yoki ibodatdir",
            "D) haj yoki ziyorat"
        ],
        "togri": "C"
    },
    {
        "savol": "Islomning uchinchi ustuni",
        "variantlar": [
            "A) haj yoki ziyorat",
            "B) savm yoki roʻzadir",
            "C) zakot",
            "D) namoz yoki ibodatdir"
        ],
        "togri": "C"
    },
    {
        "savol": "Islomning toʻrtinchi ustuni",
        "variantlar": [
            "A) haj yoki ziyorat",
            "B) savm yoki roʻzadir",
            "C) namoz yoki ibodatdir",
            "D) zakot"
        ],
        "togri": "B"
    },
    {
        "savol": "Islomning oxirgi ustuni",
        "variantlar": [
            "A) haj yoki ziyorat",
            "B) zakot",
            "C) savm yoki roʻzadir",
            "D) namoz yoki ibodatdir"
        ],
        "togri": "A"
    },
    {
        "savol": "Qur’on",
        "variantlar": [
            "A) yahudiylik dinining muqaddas kitobi",
            "B) buddaviylik dinining muqaddas kitobi",
            "C) islom dinining muqaddas kitobi",
            "D) xristianlik dinining muqaddas kitobi"
        ],
        "togri": "C"
    },
    {
        "savol": "Qur’oni Karim sahifalarini bir kitobga jamlash qachon boshlangan",
        "variantlar": [
            "A) xalifa abu bakr davrida boshlanib xalifa hazrati usmon davrida yakunlangan va to‘rt nusxada ko‘chirilgan",
            "B) xalifa usmon davrida boshlanib xalifa hazrati ali davrida yakunlangan va to‘rt nusxada ko‘chirilgan",
            "C) xalifa zayt ibn sobit davrida boshlanib xalifa hazrati ali davrida yakunlangan va to‘rt nusxada ko‘chirilgan",
            "D) xalifa abbosiylar davrida boshlanib to‘rt nusxada ko‘chirilgan"
        ],
        "togri": "A"
    },
    {
        "savol": "Qur’oni Karimda",
        "variantlar": [
            "A) 114 sura, 6236 ta oyat bor",
            "B) 112 sura, 6236 ta oyat bor",
            "C) 114 sura, 6230 ta oyat bor",
            "D) 110 sura, 6236 ta oyat bor"
        ],
        "togri": "A"
    },
    {
        "savol": "Ilohiyotda Islom dini uch elementdan",
        "variantlar": [
            "A) yolg‘ondan iborat",
            "B) axloqdan iborat",
            "C) donolikdan iborat",
            "D) iymon, Islom, ehsondan iborat"
        ],
        "togri": "D"
    },
    {
        "savol": "Iymon talablari Suniylikda quyidagi aqidalarni",
        "variantlar": [
            "A) payg‘ambarlarga",
            "B) oxirat kuniga",
            "C) Allohga, farishtalarga, muqaddas kitoblarga, payg‘ambarlarga, oxirat kuniga, taqdirning ilohiyligiga va o‘lgandan keyin tirilishga ishonish talablarini o‘z ichiga oladi",
            "D) Allohga, farishtalarga, muqaddas kitoblarga"
        ],
        "togri": "C"
    },
    {
        "savol": "Hadis arabchadan",
        "variantlar": [
            "A) Yaxshi amallar",
            "B) hikoya - Muhammad (S.A.V.) aytgan so‘zlari, qilgan ishlari, iqrorlari to‘g‘risidagi rivoyat",
            "C) xabar, gap, yangilik - Muhammad (S.A.V.) aytgan so‘zlari, qilgan ishlari, iqrorlari to‘g‘risidagi rivoyat",
            "D) halollik"
        ],
        "togri": "C"
    },
    {
        "savol": "Abu Iso Muhammad Termiziyning «Sahihi Termiziy» hadislar to‘plami 1-jildining o‘zbekcha tarjimasi",
        "variantlar": [
            "A) 1998-yil Toshkentda chop etildi",
            "B) 2000-yil Toshkentda chop etildi",
            "C) 2001-yil Toshkentda chop etildi",
            "D) 1999-yil Toshkentda chop etildi"
        ],
        "togri": "D"
    },
    {
        "savol": "Kufrga quyidagi jiddiy gunohlar kiradi",
        "variantlar": [
            "A) Allohga, farishtalarga, muqaddas kitoblarga, payg‘ambarlarga, oxirat kuniga, taqdirning ilohiyligiga va o‘lgandan keyin tirilishga ishonish talablarini o‘z ichiga oladi",
            "B) ichkilikbozlik",
            "C) shirk keltirish; namozdan voz kechish; sehrgarlik; zinokorlik; o‘z joniga qasd qilish; ichkilikbozlik; qimorbozlik",
            "D) qimorbozlik"
        ],
        "togri": "C"
    },
    {
        "savol": "kofir",
        "variantlar": [
            "A) shirk keltirish; sehrgarlik",
            "B) dinga ishonmaydigan, uni rad etuvchi",
            "C) namozdan voz kechish",
            "D) zinokorlik"
        ],
        "togri": "B"
    },
    {
        "savol": "O‘zbekiston Respublikasi «Vijdon erkinligi va diniy tashkilotlar to‘g‘risida»gi yangi tahrirdagi qonuni",
        "variantlar": [
            "A) 1991 yil 14-iyun",
            "B) 1998 yil 1 may",
            "C) 2021 yil 5 iyul",
            "D) 2020 yil 5 iyul"
        ],
        "togri": "C"
    },
    {
        "savol": "Diniy-ekstremistik xarakterdagi sektalar",
        "variantlar": [
            "A) «Beloe bratstvo», «Bojestvenniy orden Pervogo Angela»",
            "B) «Bogorodichiy sentr», «Serkov ob'edineniya»",
            "C) «Serkov Isusa», «Serkov Novogo Zaveta»",
            "D) Barchasi to‘g‘ri"
        ],
        "togri": "D"
    },
    {
        "savol": "«Aum sinrikyo» - (sanskritcha «olam»)",
        "variantlar": [
            "A) «Supreme truth», ya'ni «oliy haqiqat»",
            "B) Aum qoidasi ingliz tilida «Supreme truth», ya'ni «haqiqat»",
            "C) Aum ta'limoti; «Supreme truth», ya'ni «oliy Aum»",
            "D) Aum haqiqati ta'limoti; ingliz tilida «Supreme truth», ya'ni «oliy haqiqat»"
        ],
        "togri": "D"
    },
    {
        "savol": "«Oq birodarlik tashkiloti»",
        "variantlar": [
            "A) «Qo‘riqchi minora» bilan bog‘liq",
            "B) Janjalkash sekta, N'yu Eyj harakati bilan bog‘liq",
            "C) «Aum Sinrikyo bilan bog‘liq",
            "D) Sahrodagi bo‘ron» operatsiyasi bilan bog‘liq"
        ],
        "togri": "B"
    },
    {
        "savol": "Islom dini doirasidagi Yangi diniy harakatlar",
        "variantlar": [
            "A) Sahrodagi bo‘ron» operatsiyasi",
            "B) «Qo‘riqchi minora», «Bibliya», «Risolalar",
            "C) «Aum Sinrikyo",
            "D) «Bahoiylar», «Ahmadiylar» va «Qora musulmonlar»"
        ],
        "togri": "D"
    },
    {
        "savol": "Hinduiylik doirasidagi Yangi diniy harakatlar",
        "variantlar": [
            "A) «Xalqaro Krishnani anglash jamiyati»",
            "B) «Qo‘riqchi minora», «Bibliya», «Risolalar",
            "C) «Aum Sinrikyo",
            "D) Sahrodagi bo‘ron» operatsiyasi"
        ],
        "togri": "A"
    },
    {
        "savol": "«Iegovo shohidlari» ……… katta e'tibor beradi",
        "variantlar": [
            "A) Nyu-Yorkda, «Galaad»",
            "B) Missionerlikka",
            "C) Nyu Eyj harakatiga",
            "D) Krishnani anglashga"
        ],
        "togri": "B"
    },
    {
        "savol": "Missionerlar tayyorlash markazi",
        "variantlar": [
            "A) Nyu-Yorkda, «Galaad»",
            "B) Nyu Eyj harakati bilan bog‘liq",
            "C) Missionerlik bilan",
            "D) Krishnani anglash"
        ],
        "togri": "A"
    },
    {
        "savol": "Missionerlik faoliyatini moliyaviy qo‘llab-quvvatlash jamiyatlari",
        "variantlar": [
            "A) «Xalqaro Krishnani anglash jamiyati",
            "B) «Aum Sinrikyo",
            "C) Sahrodagi bo‘ron» operatsiyasi",
            "D) «Qo‘riqchi minora», «Bibliya», «Risolalar"
        ],
        "togri": "D"
    },
    {
        "savol": "Kibermakon …..",
        "variantlar": [
            "A) dunyo Kompyuter tarmoqlarining «virtual» umumiy majmui",
            "B) «axborot urushi»",
            "C) «Sahrodagi bo‘ron» operatsiyasi",
            "D) Missionerlar tayyorlash markazi"
        ],
        "togri": "A"
    },
    {
        "savol": "Kibermakon atamasi …… romanida qo‘llanilgan,",
        "variantlar": [
            "A) 1984 yil Uilyam Gibsonning «Neyromant» («Neuromancer»)",
            "B) 1830 yil N'yu-Yorkda Jozef Smit",
            "C) Teylor",
            "D) Devid Koresh"
        ],
        "togri": "A"
    },
    {
        "savol": "«Axborot urushi» atamasini ilk bor",
        "variantlar": [
            "A) 1984 yil Uilyam Gibsonning",
            "B) 1976 yil «Qurol tizimi va axborot urushi» hisobotida Tomas Rona ishlatgan",
            "C) 1991 yil «Sahrodagi bo‘ron» operatsiyasida ishlatildi",
            "D) 1998 yil oktyabr AQSH mudofaa vazirligi ishlatdi"
        ],
        "togri": "B"
    },
    {
        "savol": "Axborot texnologiyalari ilk marotaba harbiy harakatlar vositasi sifatida",
        "variantlar": [
            "A) 1991 yil «Sahrodagi bo‘ron» operatsiyasida ishlatildi",
            "B) 1998 yil oktyabr AQSH mudofaa vazirligi ishlatdi",
            "C) 2000 yil «Aum Sinrikyo tomonidan ishlatildi",
            "D) 2005 yil «Qo‘riqchi minora» ishlatdi"
        ],
        "togri": "A"
    },
    {
        "savol": "«Axborot urushining birlashgan doktrinasi» qachon amalga oshirildi",
        "variantlar": [
            "A) 2010 yil «Xalqaro Krishnani anglash jamiyati tomonidan",
            "B) 2000 yil «Aum Sinrikyo tomonidan",
            "C) 2005 yil «Qo‘riqchi minora», tomonidan",
            "D) 1998 yil oktyabr AQSH mudofaa vazirligi tomonidan"
        ],
        "togri": "D"
    },
    {
        "savol": "«Mafkura poligonlari yadro poligonlaridan ham ko‘proq kuchga ega». Kimga tegishli?",
        "variantlar": [
            "A) Devid Koresh",
            "B) Muller",
            "C) Teylor",
            "D) Islom Karimov"
        ],
        "togri": "D"
    },
    {
        "savol": "Kimki axborotga ega bo‘lsa .......",
        "variantlar": [
            "A) u dunyoga egalik qiladi",
            "B) shoshqaloqlik qiladi",
            "C) Xabarni tekshiradi",
            "D) bolalarni diniy tashkilotlarga jalb etadi"
        ],
        "togri": "A"
    },
    {
        "savol": "Xabarni tekshirish Allohdan, ……",
        "variantlar": [
            "A) dindorlardan majburiy yig‘im undirish va soliq olish",
            "B) (unda) shoshqaloqlik qilish shaytondandir",
            "C) axborotga ega bo‘ladi",
            "D) u dunyoga egalik qiladi"
        ],
        "togri": "B"
    },
    {
        "savol": "«Dovud avlodi» sektasini kim shakllantirgan",
        "variantlar": [
            "A) Muller",
            "B) I.Karimov",
            "C) Devid Koresh",
            "D) Teylor"
        ],
        "togri": "C"
    },
    {
        "savol": "«Osmon darvozasi» sektasi qaerda paydo bo‘lgan",
        "variantlar": [
            "A) AQSHda",
            "B) O‘zbekistonda",
            "C) Rossiyada",
            "D) Fransiyada"
        ],
        "togri": "A"
    },
    {
        "savol": "Ekstremizm -",
        "variantlar": [
            "A) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash",
            "B) tartiblar, sharoit, holat, vaziyatni hisobga olmagan holda,  urinishni anglatadi",
            "C) «aql bovar qilmas darajada», «haddan oshish»",
            "D) lotincha - «qo‘rqitish», «vahimaga solish»"
        ],
        "togri": "C"
    },
    {
        "savol": "Diniy ekstremizm -",
        "variantlar": [
            "A) tartiblar, sharoit, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "B) jamiyat uchun an’anaviy bo‘lgan diniy qadriyatlar va aqidalarni rad etish, ularga zid g‘oyalarni aldov va zo‘rlik bilan targ‘ib qilishga asoslangan nazariya va amaliyotni anglatadi",
            "C) muayyan sharoitda, biron-bir g‘oyaga qat’iy ishonib, shunga urinishni anglatadi",
            "D) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga qaratilgan jinoiy faoliyatdir"
        ],
        "togri": "B"
    },
    {
        "savol": "Fundamentalizm -",
        "variantlar": [
            "A) (lotincha - «asos») tushunchasining ma’nosi muayyan ijtimoiy hodisaning dastlabki ko‘rinishini anglatadi",
            "B) vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "C) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga",
            "D) biron-bir g‘oyaga qat’iy ishonib, vaziyatni hisobga olmagan holda, shunga urinishni anglatadi"
        ],
        "togri": "A"
    },
    {
        "savol": "Diniy fundamentalizm -",
        "variantlar": [
            "A) «ma’lum din vujudga kelgan ilk davriga qaytish va bu yo‘l bilan zamonaning barcha muammolarini hal qilish mumkin», degan fikrni ilgari surish ta’limotini anglatadi",
            "B) tartiblar, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "C) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash",
            "D) aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, qaratilgan jinoiy faoliyatdir"
        ],
        "togri": "A"
    },
    {
        "savol": "«Fundamentalizm» atamasi qaysi din bilan bog‘liq va qachon vujudga kelgan",
        "variantlar": [
            "A) muayyan sharoitda, uni mutlaqlashtirish asosida shakllangan qoida",
            "B) xristian dini bilan bog‘liq va birinchi jahon urushi arafasida vujudga kelgan",
            "C) vahima va qo‘rquv uyg‘otish, qaratilgan jinoiy faoliyatdir",
            "D) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash"
        ],
        "togri": "B"
    },
    {
        "savol": "Aqidaparastlik",
        "variantlar": [
            "A) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga",
            "B) aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, qaratilgan jinoiy faoliyatdir",
            "C) muayyan sharoitda, biron-bir g‘oyaga qat’iy ishonib, uni mutlaqlashtirish asosida shakllangan qoida va tartiblarni sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "D) lotincha - «qo‘rqitish», «vahimaga solish»"
        ],
        "togri": "C"
    },
    {
        "savol": "Mutaassiblik (arab. - «g‘uluv ketish», «chuqur ketish»)",
        "variantlar": [
            "A) ommaviy va siyosiy maqsadlarga erishish uchun zo‘ravonlikdan foydalanishdir",
            "B) (lotincha - «qo‘rqitish», «vahimaga solish»)",
            "C) o‘z fikr-mulohaza va dunyoqarashi to‘g‘riligiga o‘ta qattiq ishonib, boshqa diniy e’tiqodlarga murosasiz munosabatda bo‘lishni anglatadi",
            "D) davlatlarni beqarorlashtirishga qaratilgan siyosiy qo‘poruvchilik faoliyatini ifodalaydi"
        ],
        "togri": "C"
    },
    {
        "savol": "Terrorizm",
        "variantlar": [
            "A) davlatlar, xalqaro tashkilotlar, siyosiy partiya va harakatlarni beqarorlashtirishga qaratilgan siyosiy qo‘poruvchilik faoliyatini ifodalaydi",
            "B) ommaviy va siyosiy maqsadlarga erishish uchun zo‘ravonlikdan foydalanishdir",
            "C) (lotincha - «qo‘rqitish», «vahimaga solish») aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga qaratilgan jinoiy faoliyatdir",
            "D) xalqaro tashkilotlarni siyosiy partiya va harakatlarni faoliyatini ifodalaydi"
        ],
        "togri": "C"
    },
    {
        "savol": "Terror -",
        "variantlar": [
            "A) ommaviy va siyosiy maqsadlarga erishish uchun zo‘ravonlikdan hamda zo‘ravonlik qilish bilan tahdid solishdan muntazam foydalanishdir",
            "B) davlatlar va harakatlarni beqarorlashtirishgan siyosiy qo‘poruvchilik faoliyatidir",
            "C) xalqaro tashkilotlarni siyosiy partiya va harakatlarni faoliyatini ifodalaydi",
            "D) zo‘ravonlik qilish bilan tahdid solishdan muntazam foydalanishdir"
        ],
        "togri": "A"
    },
    {
        "savol": "Xalqaro terrorizm» tushunchasi.",
        "variantlar": [
            "A) zo‘ravonlik qilish bilan tahdid solishdan muntazam foydalanishdir",
            "B) ommaviy va siyosiy maqsadlarga erishish uchun tahdid solishdan muntazam foydalanish",
            "C) zo‘ravonlik",
            "D) davlatlar, xalqaro tashkilotlar, siyosiy partiya va harakatlarni beqarorlashtirishga qaratilgan siyosiy qo‘poruvchilik faoliyatini ifodalaydi"
        ],
        "togri": "D"
    },
    {
        "savol": "Xalqaro terrorchilik harakatlarining asosiy belgilari:",
        "variantlar": [
            "A) Davlatlar chegaralarini buzish orqali amalga oshirilishi",
            "B) Xalqaro huquq himoyasidagi ob’ekt yoki subyektlarga qarshi qaratilgani",
            "C) Barchasi to‘g‘ri",
            "D) A’zolari ikki yoki undan ortiq davlat fuqarolari, shu jumladan, yollanma Shaxslar bo‘lgan ekstremistik guruhlar tomonidan sodir etilishi"
        ],
        "togri": "C"
    },
    {
        "savol": "O‘zbekiston Respublikasining «Terrorizmga qarshi kurash to‘g‘risida»gi qonuni",
        "variantlar": [
            "A) 2005 yil 15 dekabr",
            "B) 2004 yil 26 avgust",
            "C) 1999 yil 15 dekabr",
            "D) 2000 yil 15 dekabr"
        ],
        "togri": "D"
    },
    {
        "savol": "O‘zbekiston Respublikasining «Jinoiy faoliyatdan olingan daromadlarni legallashtirishga va terrorizmni moliyalashtirishga qarshi kurash to‘g‘risida»gi Qonuni",
        "variantlar": [
            "A) 2000 yil 26 mart",
            "B) 1999 yil 15 dekabr",
            "C) 2004 yil 26 avgust",
            "D) 2005 yil 11 mart"
        ],
        "togri": "C"
    },
    {
        "savol": "BMT terrorizmga qarshi",
        "variantlar": [
            "A) 2 protokol qabul qilgan",
            "B) 15 ta rezolyutsiya, 20 konvensiya",
            "C) 18 ta rezolyutsiya, 16 konvensiya",
            "D) 12 ta rezolyutsiya, 16 konvensiya, 2 protokol qabul qilgan"
        ],
        "togri": "D"
    },
    {
        "savol": "Vazirlar Mahkamasining 130-sonli «Ijtimoiy-ma’naviy muhitni yanada sog‘lomlashtirish, diniy aqidaparastlikning oldini olish chora-tadbirlari to‘g‘risida»gi Qarori qachon qabul qilingan.",
        "variantlar": [
            "A) 2005 yil 26 martda",
            "B) 1999 yil 21 martda",
            "C) 2000 yil 26 martda",
            "D) 1998 yil 26 martda"
        ],
        "togri": "D"
    },
    {
        "savol": "«Vijdon erkinligi va diniy tashkilotlar to‘g‘risida»gi Qonunning 19-moddasi ……",
        "variantlar": [
            "A) diniy ekstremizm, separatizm va aqidaparastlik g‘oyalari bilan yo‘g‘rilgan matbaa nashrlar,",
            "B) Barchasi to‘g‘ri",
            "C) kino, foto, audio, video mahsulotlari va shu kabi boshqa mahsulotlarni tayyorlash, saqlash va tarqatish",
            "D) muayyan javobgarlikka olib kelishi mumkinligini nazarda tutadi"
        ],
        "togri": "B"
    },
    {
        "savol": "SАHОBАLАR - (yohud аs-sаhоbа, sоhib -",
        "variantlar": [
            "A) Barchasi to‘g‘ri",
            "B) «tаrаfdоr»ning ko‘pligi - аsхоb)",
            "C) Muhаmmаd (s.а.v)ning sаfdоshlаri, u zоt bilаn mulоqоtdа bo‘lgаn yohud g‘аzоtlаridа qаtnаshgаn kishilаr",
            "D) Muhаmmаd (s.а.v.)ni lоqаl bir mаrоtаbа, gаrchi go‘dаklik chоg‘idа bo‘lsа hаm ko‘rgаn bаrchа kishilаr"
        ],
        "togri": "A"
    },
    {
        "savol": "Hadis 2 turga -",
        "variantlar": [
            "A) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»",
            "B) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi",
            "C) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi",
            "D) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi"
        ],
        "togri": "C"
    },
    {
        "savol": "Birinchi hadis kitobini kim yozdi",
        "variantlar": [
            "A) Burxoniddin Marginoniy",
            "B) Ibn Shihob az-Zuhriy",
            "C) At-Termiziy",
            "D) Al Buxoriy"
        ],
        "togri": "B"
    },
    {
        "savol": "Hijriy 3-asrda hadis tahlil etish sohasida",
        "variantlar": [
            "A) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi",
            "B) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi",
            "C) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»",
            "D) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi"
        ],
        "togri": "A"
    },
    {
        "savol": "9- 10-asr boshlarida eng ishonchli deb tanilgan hadisning 6 ta to‘plami vujudga kelgan.",
        "variantlar": [
            "A) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi",
            "B) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»",
            "C) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi",
            "D) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi"
        ],
        "togri": "B"
    },
    {
        "savol": "Hanafiylik mazhabining asoschisi",
        "variantlar": [
            "A) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy",
            "B) Molik ibn Anas",
            "C) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "D) Ahmad ibn Hanbal"
        ],
        "togri": "C"
    },
    {
        "savol": "Molikiylik mazhabining asoschisi",
        "variantlar": [
            "A) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "B) Molik ibn Anas",
            "C) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy",
            "D) Ahmad ibn Hanbal"
        ],
        "togri": "B"
    },
    {
        "savol": "Shofe’iy mazhabining asoschisi",
        "variantlar": [
            "A) Ahmad ibn Hanbal",
            "B) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "C) Molik ibn Anas",
            "D) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy"
        ],
        "togri": "D"
    },
    {
        "savol": "Hanbaliy mazhabining asoschisi",
        "variantlar": [
            "A) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy",
            "B) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "C) Molik ibn Anas",
            "D) Ahmad ibn Hanbal"
        ],
        "togri": "D"
    },
    {
        "savol": "Yangi diniy harakatlar ........",
        "variantlar": [
            "A) XX asr 80-yillar Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar",
            "B) XX asr 60-yillar Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar",
            "C) XX asrning 70-yillarida Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar va oqimlar",
            "D) XX asr 50-yillarida Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar"
        ],
        "togri": "C"
    },
    {
        "savol": "«Kitobi al-Jom’e as-saxix», «Kitob ul ilm», «Kitobi at-Tamoyili an-Nabaviy», «Kitobi az-zuxl», «Kitobul ismi val xuna» kabi asarlar muallifi kim",
        "variantlar": [
            "A) Burxoniddin Marginoniy",
            "B) Ibn Shihob az-Zuhriy",
            "C) At-Termiziy",
            "D) Al Buxoriy"
        ],
        "togri": "C"
    },
    {
        "savol": "«Xidoya fi furu’ al-fukx» (Fikx sohalari bo‘yicha qo‘llanma) kim yozgan",
        "variantlar": [
            "A) Burxoniddin Marginoniy",
            "B) At-Termiziy",
            "C) Ibn Shihob az-Zuhriy",
            "D) Al Buxoriy"
        ],
        "togri": "A"
    },
    {
        "savol": "Aqida arab tilidan «aqd»",
        "variantlar": [
            "A) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi",
            "B) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»",
            "C) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi",
            "D) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi"
        ],
        "togri": "C"
    },
    {
        "savol": "Imonsizlik",
        "variantlar": [
            "A) vijdоnsizlik, e’tiqоdsizlik, tubаn yo‘llаrgа yurish, аxlоq, оdоb, insоnpаrvаrlik qоidа vа tаlаblаrigа riоya qilmаslik",
            "B) maxluqni Robbil olamiynga 5 ishdan birida tenglashtirishdir.",
            "C) Alloh taologa xos bo‘lgan sifatlarni Undan o‘zgaga sobit qilish (ko‘chirish)dir",
            "D) ibodatda shirk keltirish; duoda shirk keltirish; robbilikda shirk keltirish;"
        ],
        "togri": "A"
    },
    {
        "savol": "Shirk arabcha -",
        "variantlar": [
            "A) sherik keltirish, Allohning sherigi bor deb e’tiqod qilish, Alloh taologa xos bo‘lgan sifatlarni Undan o‘zgaga sobit qilish (ko‘chirish)dir",
            "B) vijdоnsizlik, tubаn yo‘llаrgа yurish, аxlоq, qоidа vа tаlаblаrigа riоya qilmаslik",
            "C) maxluqni Robbil olamiynga 5 ishdan birida tenglashtirishdir.",
            "D) mulk va sultondagi shirk keltirish; xalq-yaratishdagi shirk keltirish;"
        ],
        "togri": "A"
    },
    {
        "savol": "Shirkning shar’iy tushunchasi -",
        "variantlar": [
            "A) e’tiqоdsizlik, аxlоq, оdоb, insоnpаrvаrlik qоidа vа tаlаblаrigа riоya qilmаslik",
            "B) Alloh taologa xos bo‘lgan sifatlarni Undan o‘zgaga sobit qilish (ko‘chirish)dir",
            "C) maxluqni Robbil olamiynga 5 ishdan birida tenglashtirishdir. Ya’ni, Allohning zotida, sifatlarida, ismlarida, ishlarida va hukmlarida sherigi bor, deb e’tiqod qilishdir",
            "D) mulkdagi shirk keltirish; xalq-yaratishdagi shirk keltirish; itoatda shirk keltirish"
        ],
        "togri": "C"
    },
    {
        "savol": "Sunnat -",
        "variantlar": [
            "A) Islomdagi eng ko‘p tarqalgan mazhabdir",
            "B) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "C) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish",
            "D) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari"
        ],
        "togri": "D"
    },
    {
        "savol": "Ijmo -",
        "variantlar": [
            "A) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari",
            "B) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "C) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish",
            "D) Islomdagi eng ko‘p tarqalgan mazhabdir"
        ],
        "togri": "B"
    },
    {
        "savol": "Qiyos -",
        "variantlar": [
            "A) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari",
            "B) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish",
            "C) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "D) Islomdagi eng ko‘p tarqalgan mazhabdir"
        ],
        "togri": "B"
    },
    {
        "savol": "Hanafiylik",
        "variantlar": [
            "A) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "B) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari",
            "C) Islomdagi eng ko‘p tarqalgan mazhabdir",
            "D) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish"
        ],
        "togri": "C"
    },
    {
        "savol": "Imom Buxoriy hayoti davomida",
        "variantlar": [
            "A) 600 ming hadis to‘plab, ulardan 7275 hadisni o‘zining 5 jildlik «Ishonarli to‘plam»iga kiritdi",
            "B) 650 ming hadis to‘plab, ulardan 7275 hadisni o‘zining 4 jildlik «Ishonarli to‘plam»iga kiritdi",
            "C) 600 ming hadis to‘plab, ulardan 7175 hadisni o‘zining 4 jildlik «Ishonarli to‘plam»iga kiritdi",
            "D) 600 ming hadis to‘plab, ulardan 7275 hadisni o‘zining 4 jildlik «Ishonarli to‘plam»iga kiritdi"
        ],
        "togri": "D"
    },
    {
        "savol": "Shariat -",
        "variantlar": [
            "A) «ahira» so‘zidan «oxir», «keyin bo‘ladigan narsa», «oxirgi kun» degan ma’nolarni bildiradi.",
            "B) «yo‘nalish» ma'nosini bildirib, Islom atamashunosligida biror diniy masala, muammo bo‘yicha muayyan ulamo fikriga ergashish",
            "C) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun.",
            "D) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, ibodat yo‘llari, hayotiy va ijtimoiy qoidalar, kishilar orasidagi munosabat va muammolar, halol bilan haromni ajratib bermoqdir"
        ],
        "togri": "D"
    },
    {
        "savol": "Mazhab so‘zi (arabcha - zaxaba 'ala mazhabixi)",
        "variantlar": [
            "A) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, ibodat yo‘llari, hayotiy va ijtimoiy qoidalar, kishilar orasidagi munosabat va muammolar, halol bilan haromni ajratib bermoqdir",
            "B) «yo‘nalish» ma'nosini bildirib, Islom atamashunosligida biror diniy masala, muammo bo‘yicha muayyan ulamo fikriga ergashish, «uning yurgan yo‘nalishidan borish» ni bildiradi",
            "C) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun. Qiyomat kuniga iymon keltirish islom dinining muhim unsurlaridan biridir",
            "D) «ahira» so‘zidan «oxir», «keyin bo‘ladigan narsa», «oxirgi kun» degan ma’nolarni bildiradi. Musulmonlar bu so‘zni bu yerdagi dunyoning oxiri, shuningdek, o‘limdan keyin boshlanadigan yangi, cheksiz hayot deb atashadi"
        ],
        "togri": "B"
    },
    {
        "savol": "Oxirat arabcha",
        "variantlar": [
            "A) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, ibodat yo‘llari, kishilar orasidagi munosabat va muammolar, halol bilan haromni ajratib bermoqdir",
            "B) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun.",
            "C) «yo‘nalish» ma'nosini bildirib, Islom atamashunosligida biror diniy masala, «uning yurgan yo‘nalishidan borish» ni bildiradi",
            "D) «ahira» so‘zidan «oxir», «keyin bo‘ladigan narsa», «oxirgi kun» degan ma’nolarni bildiradi. Musulmonlar bu so‘zni bu yerdagi dunyoning oxiri, shuningdek, o‘limdan keyin boshlanadigan yangi, cheksiz hayot deb atashadi"
        ],
        "togri": "D"
    },
    {
        "savol": "«Qiyomat» arabcha",
        "variantlar": [
            "A) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun. Qiyomat kuniga iymon keltirish islom dinining muhim unsurlaridan biridir",
            "B) . Musulmonlar bu so‘zni bu yerdagi dunyoning oxiri, shuningdek, o‘limdan keyin boshlanadigan yangi cheksiz hayot deb atashadi",
            "C) Islom atamashunosligida biror diniy masala, muammo bo‘yicha muayyan ulamo fikriga ergashish",
            "D) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, halol bilan haromni ajratib bermoqdir"
        ],
        "togri": "A"
    },
    {
        "savol": "Molikiylikning kitobi",
        "variantlar": [
            "A) «Al-Muvatta»",
            "B) «Al-Umm»",
            "C) «Al-Musnad»",
            "D) «Al-Kofiy»"
        ],
        "togri": "A"
    },
    {
        "savol": "Shofe'iylikning kitobi",
        "variantlar": [
            "A) «Al-Kofiy»",
            "B) «Al-Muvatta»",
            "C) «Al-Musnad»",
            "D) «Al-Umm»"
        ],
        "togri": "D"
    },
    {
        "savol": "Hanbaliylikning kitobi",
        "variantlar": [
            "A) «Al-Kofiy»",
            "B) «Al-Muvatta»",
            "C) «Al-Umm»",
            "D) «Al-Musnad»"
        ],
        "togri": "D"
    },
    {
        "savol": "Din so‘zining ma’nosi…",
        "variantlar": [
            "A) e’tiqod - ibodat",
            "B) jannatga qaytish",
            "C) ishonch - e’tiqod",
            "D) e’tiqod - zakot"
        ],
        "togri": "C"
    },
    {
        "savol": "Hinduiylik doirasidagi Yangi diniy harakatlar",
        "variantlar": [
            "A) «Qo‘riqchi minora», «Bibliya», «Risolalar",
            "B) «Xalqaro Krishnani anglash jamiyati»",
            "C) «Aum Sinrikyo",
            "D) Sahrodagi bo‘ron» operatsiyasi"
        ],
        "togri": "B"
    },
    {
        "savol": "«Iegovo shohidlari» ……… katta e'tibor beradi",
        "variantlar": [
            "A) Missionerlikka",
            "B) Nyu-Yorkda, «Galaad»",
            "C) Nyu Eyj harakatiga",
            "D) Krishnani anglashga"
        ],
        "togri": "A"
    },
    {
        "savol": "Missionerlar tayyorlash markazi",
        "variantlar": [
            "A) Nyu Eyj harakati bilan bog‘liq",
            "B) Nyu-Yorkda, «Galaad»",
            "C) Missionerlik bilan",
            "D) Krishnani anglash"
        ],
        "togri": "B"
    },
    {
        "savol": "Missionerlik faoliyatini moliyaviy qo‘llab-quvvatlash jamiyatlari",
        "variantlar": [
            "A) «Aum Sinrikyo",
            "B) «Qo‘riqchi minora», «Bibliya», «Risolalar",
            "C) Sahrodagi bo‘ron» operatsiyasi",
            "D) «Xalqaro Krishnani anglash jamiyati"
        ],
        "togri": "B"
    },
    {
        "savol": "Kibermakon …..",
        "variantlar": [
            "A) dunyo Kompyuter tarmoqlarining «virtual» umumiy majmui (maydoni)",
            "B) «axborot urushi»",
            "C) «Sahrodagi bo‘ron» operatsiyasi",
            "D) Missionerlar tayyorlash markazi"
        ],
        "togri": "A"
    },
    {
        "savol": "Kibermakon atamasi …… romanida qo‘llanilgan,",
        "variantlar": [
            "A) 1984 yil Uilyam Gibsonning «Neyromant» («Neuromancer»)",
            "B) 1830 yil N'yu-Yorkda Jozef Smit",
            "C) Teylor",
            "D) Devid Koresh"
        ],
        "togri": "A"
    },
    {
        "savol": "Axborot texnologiyalari ilk marotaba harbiy harakatlar vositasi sifatida",
        "variantlar": [
            "A) 2000 yil «Aum Sinrikyo tomonidan ishlatildi",
            "B) 1998 yil oktyabr AQSH mudofaa vazirligi ishlatdi",
            "C) 1991 yil «Sahrodagi bo‘ron» operatsiyasida ishlatildi",
            "D) 2005 yil «Qo‘riqchi minora» ishlatdi"
        ],
        "togri": "C"
    },
    {
        "savol": "«Mafkura poligonlari yadro poligonlaridan ham ko‘proq kuchga ega». Kimga tegishli?",
        "variantlar": [
            "A) Teylor",
            "B) Muller",
            "C) Islom Karimov",
            "D) Devid Koresh"
        ],
        "togri": "C"
    },
    {
        "savol": "Kimki axborotga ega bo‘lsa .......",
        "variantlar": [
            "A) u dunyoga egalik qiladi",
            "B) shoshqaloqlik qiladi",
            "C) Xabarni tekshiradi",
            "D) bolalarni diniy tashkilotlarga jalb etadi"
        ],
        "togri": "A"
    },
    {
        "savol": "Xabarni tekshirish Allohdan, ……",
        "variantlar": [
            "A) u dunyoga egalik qiladi",
            "B) dindorlardan majburiy yig‘im undirish va soliq olish",
            "C) axborotga ega bo‘ladi",
            "D) (unda) shoshqaloqlik qilish shaytondandir"
        ],
        "togri": "D"
    },
    {
        "savol": "«Dovud avlodi» sektasini kim shakllantirgan",
        "variantlar": [
            "A) Devid Koresh",
            "B) I.Karimov",
            "C) Muller",
            "D) Teylor"
        ],
        "togri": "A"
    },
    {
        "savol": "«Osmon darvozasi» sektasi qaerda paydo bo‘lgan",
        "variantlar": [
            "A) AQSHda",
            "B) O‘zbekistonda",
            "C) «Qo‘riqchi minora», «Bibliya», «Risolalar",
            "D) «Xalqaro Krishnani anglash jamiyati"
        ],
        "togri": "A"
    },
    {
        "savol": "«O‘zbekiston Respublikasining Ma’muriy javobgarlik to‘g‘risidagi kodeksi»da",
        "variantlar": [
            "A) voyaga yetmagan bolalarni diniy tashkilotlarga jalb etish",
            "B) voyaga yetmagan bolalarni ularning ixtiyoriga, ota-onalari yoki ularning o‘rnini bosuvchi shaxslar ixtiyoriga zid tarzda dinga o‘qitish",
            "C) dindorlardan majburiy yig‘im undirish va soliq olish",
            "D) barchasi to‘g‘ri"
        ],
        "togri": "D"
    },
    {
        "savol": "Ekstremizm -",
        "variantlar": [
            "A) «aql bovar qilmas darajada», «haddan oshish»",
            "B) tartiblar, sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "C) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga",
            "D) lotincha - «qo‘rqitish», «vahimaga solish»"
        ],
        "togri": "A"
    },
    {
        "savol": "Diniy ekstremizm -",
        "variantlar": [
            "A) jamiyat uchun an’anaviy bo‘lgan diniy qadriyatlar va aqidalarni rad etish, ularga zid g‘oyalarni aldov va zo‘rlik bilan targ‘ib qilishga asoslangan nazariya va amaliyotni anglatadi",
            "B) tartiblar, sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "C) muayyan sharoitda, biron-bir g‘oyaga qat’iy ishonib, uni mutlaqlashtirish asosida shakllangan qoida va tartiblarni sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "D) aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga qaratilgan jinoiy faoliyatdir"
        ],
        "togri": "A"
    },
    {
        "savol": "Fundamentalizm -",
        "variantlar": [
            "A) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga",
            "B) tartiblar, sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "C) (lotincha - «asos») tushunchasining ma’nosi muayyan ijtimoiy hodisaning dastlabki ko‘rinishini anglatadi",
            "D) muayyan sharoitda, biron-bir g‘oyaga qat’iy ishonib, uni mutlaqlashtirish asosida shakllangan qoida va tartiblarni sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi"
        ],
        "togri": "C"
    },
    {
        "savol": "Diniy fundamentalizm -",
        "variantlar": [
            "A) «ma’lum din vujudga kelgan ilk davriga qaytish va bu yo‘l bilan zamonaning barcha muammolarini hal qilish mumkin», degan fikrni ilgari surish ta’limotini anglatadi",
            "B) tartiblar, sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi",
            "C) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga",
            "D) aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga qaratilgan jinoiy faoliyatdir"
        ],
        "togri": "A"
    },
    {
        "savol": "«Fundamentalizm» atamasi qaysi din bilan bog‘liq va qachon vujudga kelgan",
        "variantlar": [
            "A) aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, qaratilgan jinoiy faoliyatdir",
            "B) muayyan sharoitda, biron-bir g‘oyaga qat’iy ishonib, uni mutlaqlashtirish asosida shakllangan qoida",
            "C) xristian dini bilan bog‘liq va birinchi jahon urushi arafasida vujudga kelgan",
            "D) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga"
        ],
        "togri": "C"
    },
    {
        "savol": "Aqidaparastlik",
        "variantlar": [
            "A) lotincha - «qo‘rqitish», «vahimaga solish»",
            "B) aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, qaratilgan jinoiy faoliyatdir",
            "C) jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga",
            "D) muayyan sharoitda, biron-bir g‘oyaga qat’iy ishonib, uni mutlaqlashtirish asosida shakllangan qoida va tartiblarni sharoit, holat, vaziyatni hisobga olmagan holda, ko‘r-ko‘rona qo‘llash yoki shunga urinishni anglatadi"
        ],
        "togri": "D"
    },
    {
        "savol": "Mutaassiblik (arab. - «g‘uluv ketish», «chuqur ketish»)",
        "variantlar": [
            "A) (lotincha - «qo‘rqitish», «vahimaga solish»)",
            "B) o‘z fikr-mulohaza va dunyoqarashi to‘g‘riligiga o‘ta qattiq ishonib, boshqa diniy e’tiqodlarga murosasiz munosabatda bo‘lishni anglatadi",
            "C) ommaviy va siyosiy maqsadlarga erishish uchun zo‘ravonlikdan foydalanishdir",
            "D) davlatlarni beqarorlashtirishga qaratilgan siyosiy qo‘poruvchilik faoliyatini ifodalaydi"
        ],
        "togri": "B"
    },
    {
        "savol": "Terrorizm",
        "variantlar": [
            "A) ommaviy va siyosiy maqsadlarga erishish uchun zo‘ravonlikdan foydalanishdir",
            "B) (lotincha - «qo‘rqitish», «vahimaga solish») aholining keng qatlamlarida vahima va qo‘rquv uyg‘otish, jamiyatda beqarorlik keltirib chiqarish orqali davlat hokimiyatini egallash maqsadiga qaratilgan jinoiy faoliyatdir",
            "C) davlatlar, xalqaro tashkilotlar, siyosiy partiya va harakatlarni beqarorlashtirishga qaratilgan siyosiy qo‘poruvchilik faoliyatini ifodalaydi",
            "D) xalqaro tashkilotlarni siyosiy partiya va harakatlarni faoliyatini ifodalaydi"
        ],
        "togri": "B"
    },
    {
        "savol": "Terror -",
        "variantlar": [
            "A) ommaviy va siyosiy maqsadlarga erishish uchun zo‘ravonlikdan hamda zo‘ravonlik qilish bilan tahdid solishdan muntazam foydalanishdir",
            "B) davlatlar, xalqaro tashkilotlar, siyosiy partiya va harakatlarni beqarorlashtirishga qaratilgan siyosiy qo‘poruvchilik faoliyatini ifodalaydi",
            "C) xalqaro tashkilotlarni siyosiy partiya va harakatlarni faoliyatini ifodalaydi",
            "D) zo‘ravonlik qilish bilan tahdid solishdan muntazam foydalanishdir"
        ],
        "togri": "A"
    },
    {
        "savol": "Xalqaro terrorizm» tushunchasi.",
        "variantlar": [
            "A) ommaviy va siyosiy maqsadlarga erishish uchun zo‘ravonlikdan hamda zo‘ravonlik qilish bilan tahdid solishdan muntazam foydalanishdir",
            "B) davlatlar, xalqaro tashkilotlar, siyosiy partiya va harakatlarni beqarorlashtirishga qaratilgan siyosiy qo‘poruvchilik faoliyatini ifodalaydi",
            "C) zo‘ravonlik",
            "D) zo‘ravonlik qilish bilan tahdid solishdan muntazam foydalanishdir"
        ],
        "togri": "B"
    },
    {
        "savol": "Xalqaro terrorchilik harakatlarining asosiy belgilari:",
        "variantlar": [
            "A) Davlatlar chegaralarini buzish orqali amalga oshirilishi",
            "B) Xalqaro huquq himoyasidagi ob’ekt yoki subyektlarga qarshi qaratilgani",
            "C) Barchasi to‘g‘ri",
            "D) A’zolari ikki yoki undan ortiq davlat fuqarolari, shu jumladan, yollanma Shaxslar bo‘lgan ekstremistik guruhlar tomonidan sodir etilishi"
        ],
        "togri": "C"
    },
    {
        "savol": "O‘zbekiston Respublikasining «Terrorizmga qarshi kurash to‘g‘risida»gi qonuni",
        "variantlar": [
            "A) 2000 yil 15 dekabr",
            "B) 2004 yil 26 avgust",
            "C) 1999 yil 15 dekabr",
            "D) 2005 yil 15 dekabr"
        ],
        "togri": "A"
    },
    {
        "savol": "O‘zbekiston Respublikasining «Jinoiy faoliyatdan olingan daromadlarni legallashtirishga va terrorizmni moliyalashtirishga qarshi kurash to‘g‘risida»gi Qonuni",
        "variantlar": [
            "A) 2005 yil 11 mart",
            "B) 1999 yil 15 dekabr",
            "C) 2000 yil 26 mart",
            "D) 2004 yil 26 avgust"
        ],
        "togri": "D"
    },
    {
        "savol": "BMT terrorizmga qarshi",
        "variantlar": [
            "A) 2 protokol qabul qilgan",
            "B) 15 ta rezolyutsiya, 20 konvensiya",
            "C) 18 ta rezolyutsiya, 16 konvensiya",
            "D) 12 ta rezolyutsiya, 16 konvensiya, 2 protokol qabul qilgan"
        ],
        "togri": "D"
    },
    {
        "savol": "Vazirlar Mahkamasining 130-sonli «Ijtimoiy-ma’naviy muhitni yanada sog‘lomlashtirish, diniy aqidaparastlikning oldini olish chora-tadbirlari to‘g‘risida»gi Qarori qachon qabul qilingan.",
        "variantlar": [
            "A) 2000 yil 26 martda",
            "B) 1999 yil 21 martda",
            "C) 1998 yil 26 martda",
            "D) 2005 yil 26 martda"
        ],
        "togri": "C"
    },
    {
        "savol": "«Vijdon erkinligi va diniy tashkilotlar to‘g‘risida»gi Qonunning 19-moddasi ……",
        "variantlar": [
            "A) kino, foto, audio, video mahsulotlari va shu kabi boshqa mahsulotlarni tayyorlash, saqlash va tarqatish",
            "B) diniy ekstremizm, separatizm va aqidaparastlik g‘oyalari bilan yo‘g‘rilgan matbaa nashrlar,",
            "C) Barchasi to‘g‘ri",
            "D) muayyan javobgarlikka olib kelishi mumkinligini nazarda tutadi"
        ],
        "togri": "C"
    },
    {
        "savol": "SАHОBАLАR - (yohud аs-sаhоbа, sоhib -",
        "variantlar": [
            "A) Barchasi to‘g‘ri",
            "B) «tаrаfdоr»ning ko‘pligi - аsхоb)",
            "C) Muhаmmаd (s.а.v)ning sаfdоshlаri, u zоt bilаn mulоqоtdа bo‘lgаn yohud g‘аzоtlаridа qаtnаshgаn kishilаr",
            "D) Muhаmmаd (s.а.v.)ni lоqаl bir mаrоtаbа, gаrchi go‘dаklik chоg‘idа bo‘lsа hаm ko‘rgаn bаrchа kishilаr"
        ],
        "togri": "A"
    },
    {
        "savol": "Hadis 2 turga -",
        "variantlar": [
            "A) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi",
            "B) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi",
            "C) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»",
            "D) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi"
        ],
        "togri": "B"
    },
    {
        "savol": "Birinchi hadis kitobini kim yozdi",
        "variantlar": [
            "A) Al Buxoriy",
            "B) Burxoniddin Marginoniy",
            "C) At-Termiziy",
            "D) Ibn Shihob az-Zuhriy"
        ],
        "togri": "D"
    },
    {
        "savol": "Hijriy 3-asrda hadis tahlil etish sohasida",
        "variantlar": [
            "A) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi",
            "B) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi",
            "C) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»",
            "D) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi"
        ],
        "togri": "B"
    },
    {
        "savol": "9- 10-asr boshlarida eng ishonchli deb tanilgan hadisning 6 ta to‘plami vujudga kelgan.",
        "variantlar": [
            "A) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi",
            "B) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi",
            "C) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi",
            "D) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»"
        ],
        "togri": "D"
    },
    {
        "savol": "Hanafiylik mazhabining asoschisi",
        "variantlar": [
            "A) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy",
            "B) Molik ibn Anas",
            "C) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "D) Ahmad ibn Hanbal"
        ],
        "togri": "C"
    },
    {
        "savol": "Molikiylik mazhabining asoschisi",
        "variantlar": [
            "A) Molik ibn Anas",
            "B) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "C) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy",
            "D) Ahmad ibn Hanbal"
        ],
        "togri": "A"
    },
    {
        "savol": "Shofe’iy mazhabining asoschisi",
        "variantlar": [
            "A) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "B) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy",
            "C) Molik ibn Anas",
            "D) Ahmad ibn Hanbal"
        ],
        "togri": "B"
    },
    {
        "savol": "Hanbaliy mazhabining asoschisi",
        "variantlar": [
            "A) Ahmad ibn Hanbal",
            "B) No‘mon ibn Sobit al-Kufiy Abu Hanifa",
            "C) Molik ibn Anas",
            "D) Muhammad ibn Idris ibn al-Abbos ibn Usmon ibn Shofe'iy"
        ],
        "togri": "A"
    },
    {
        "savol": "Yangi diniy harakatlar ........",
        "variantlar": [
            "A) XIX asrning 60-yillarida Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar va oqimlar",
            "B) XX asrning 70-yillarida Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar va oqimlar",
            "C) XI asrning 80-yillarida Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar va oqimlar",
            "D) X asrning 50-yillarida Yevropa va AQSHda tarqalgan noan'anaviy diniy guruhlar va oqimlar"
        ],
        "togri": "B"
    },
    {
        "savol": "«Kitob ul ilm», «Kitobi at-Tamoyili an-Nabaviy», «Kitobi az-zuxl», «Kitobul ismi val xuna» kabi asarlar muallifi kim",
        "variantlar": [
            "A) Burxoniddin Marginoniy",
            "B) Ibn Shihob az-Zuhriy",
            "C) At-Termiziy",
            "D) Al Buxoriy"
        ],
        "togri": "C"
    },
    {
        "savol": "«Xidoya fi furu’ al-fukx» (Fikx sohalari bo‘yicha qo‘llanma) kim yozgan",
        "variantlar": [
            "A) At-Termiziy",
            "B) Burxoniddin Marginoniy",
            "C) Ibn Shihob az-Zuhriy",
            "D) Al Buxoriy"
        ],
        "togri": "B"
    },
    {
        "savol": "Aqida arab tilidan «aqd»",
        "variantlar": [
            "A) hadisi qudsiy (ma’nosi Alloh taoloniki, aytilishi rasululloh tomonidan bo‘lgan hadislar) va hadisi nabaviyga bo‘linadi",
            "B) «Sahihi Buxoriy», «Sahihi Muslim» «Sahihi Termiziy», «Sunani Abi Dovud», «Sunani Ibn Moja», «Sunani Nasoiy»",
            "C) bir narsani ikkinchisiga mahkam bog‘lash, bir-biriga bog`lash ma’nosini anglatadi",
            "D) «musnad», «sahih», «sunan» deb atalmish turli yo‘nalishlar vujudga keldi"
        ],
        "togri": "C"
    },
    {
        "savol": "Imonsizlik",
        "variantlar": [
            "A) sherik keltirish, Allohning sherigi bor deb e’tiqod qilish, Alloh taologa xos bo‘lgan sifatlarni Undan o‘zgaga sobit qilish (ko‘chirish)dir",
            "B) maxluqni Robbil olamiynga 5 ishdan birida tenglashtirishdir. Ya’ni, Allohning zotida, sifatlarida, ismlarida, ishlarida va hukmlarida sherigi bor, deb e’tiqod qilishdir",
            "C) vijdоnsizlik, e’tiqоdsizlik, tubаn yo‘llаrgа yurish, аxlоq, оdоb, insоnpаrvаrlik qоidа vа tаlаblаrigа riоya qilmаslik",
            "D) ibodatda shirk keltirish; duoda shirk keltirish; robbilikda shirk keltirish; hukmda shirk keltirish; mulk va sultondagi shirk keltirish; xalq-yaratishdagi shirk keltirish; itoatda shirk keltirish"
        ],
        "togri": "C"
    },
    {
        "savol": "Shirk arabcha -",
        "variantlar": [
            "A) sherik keltirish, Allohning sherigi bor deb e’tiqod qilish, Alloh taologa xos bo‘lgan sifatlarni Undan o‘zgaga sobit qilish (ko‘chirish)dir",
            "B) vijdоnsizlik, e’tiqоdsizlik, tubаn yo‘llаrgа yurish, аxlоq, оdоb, insоnpаrvаrlik qоidа vа tаlаblаrigа riоya qilmаslik",
            "C) maxluqni Robbil olamiynga 5 ishdan birida tenglashtirishdir. Ya’ni, Allohning zotida, sifatlarida, ismlarida, ishlarida va hukmlarida sherigi bor, deb e’tiqod qilishdir",
            "D) ibodatda shirk keltirish; duoda shirk keltirish; robbilikda shirk keltirish; hukmda shirk keltirish; mulk va sultondagi shirk keltirish; xalq-yaratishdagi shirk keltirish; itoatda shirk keltirish"
        ],
        "togri": "A"
    },
    {
        "savol": "Shirkning shar’iy tushunchasi -",
        "variantlar": [
            "A) vijdоnsizlik, e’tiqоdsizlik, tubаn yo‘llаrgа yurish, аxlоq, оdоb, insоnpаrvаrlik qоidа vа tаlаblаrigа riоya qilmаslik",
            "B) sherik keltirish, Allohning sherigi bor deb e’tiqod qilish, Alloh taologa xos bo‘lgan sifatlarni Undan o‘zgaga sobit qilish (ko‘chirish)dir",
            "C) maxluqni Robbil olamiynga 5 ishdan birida tenglashtirishdir. Ya’ni, Allohning zotida, sifatlarida, ismlarida, ishlarida va hukmlarida sherigi bor, deb e’tiqod qilishdir",
            "D) ibodatda shirk keltirish; duoda shirk keltirish; robbilikda shirk keltirish; hukmda shirk keltirish; mulk va sultondagi shirk keltirish; xalq-yaratishdagi shirk keltirish; itoatda shirk keltirish"
        ],
        "togri": "C"
    },
    {
        "savol": "Sunnat -",
        "variantlar": [
            "A) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "B) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari",
            "C) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish",
            "D) Islomdagi eng ko‘p tarqalgan mazhabdir"
        ],
        "togri": "B"
    },
    {
        "savol": "Ijmo -",
        "variantlar": [
            "A) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish",
            "B) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari",
            "C) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "D) Islomdagi eng ko‘p tarqalgan mazhabdir"
        ],
        "togri": "C"
    },
    {
        "savol": "Qiyos -",
        "variantlar": [
            "A) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari",
            "B) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish",
            "C) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "D) Islomdagi eng ko‘p tarqalgan mazhabdir"
        ],
        "togri": "B"
    },
    {
        "savol": "Hanafiylik",
        "variantlar": [
            "A) Islomdagi eng ko‘p tarqalgan mazhabdir",
            "B) Muhammad (S.A.V.) qilgan ishlari va aytgan so‘zlari",
            "C) bir davrning ijtihod (diniy manbalardan mustaqil hukm chiqarish) darajasiga yetgan ulamolarining yakdillik bilan biror masalani qabul qilishlaridir",
            "D) hukmi vorid bo‘lmagan masalani Qur'on va hadisda, shunga o‘xshash va hukmi kelgan narsaga qiyoslab fatvo chiqarish"
        ],
        "togri": "A"
    },
    {
        "savol": "Soxta xristian harakatlar -",
        "variantlar": [
            "A) «Mun birlashtirish cherkovi», «Vissarion oxirgi Ahdi cherkovi», «Oq birodarlar»",
            "B) «Xristian ilmi», «Ron Xabbard sayentologiya markazi», «Kloneyd», «Oq ekologlar» harakati",
            "C) «Tirik axloq» (Agni yoga), «Krishnani anglash jamiyati», «Transsendental' meditasiya», «Aum-Sinrikyo», «Saxadja-yoga»",
            "D) «Runvira» ukrain milliy e'tiqodi cherkovi, Rossiya jarangli kedrlari, Omsk «qadimgi diniy e'tiqodiga qaytish kul'ti»"
        ],
        "togri": "A"
    },
    {
        "savol": "Sayentologik kul'tlar -",
        "variantlar": [
            "A) «Tirik axloq» (Agni yoga), «Krishnani anglash jamiyati», «Transsendental' meditasiya», «Aum-Sinrikyo», «Saxadja-yoga»",
            "B) «Mun birlashtirish cherkovi», «Vissarion oxirgi Ahdi cherkovi», «Oq birodarlar»",
            "C) «Xristian ilmi», «Ron Xabbard sayentologiya markazi», «Kloneyd», «Oq ekologlar» harakati",
            "D) «Runvira» ukrain milliy e'tiqodi cherkovi, Rossiya jarangli kedrlari, Omsk «qadimgi diniy e'tiqodiga qaytish kul'ti»"
        ],
        "togri": "C"
    },
    {
        "savol": "Neo va kvaziorientalistik maktablar va kul'tlar -",
        "variantlar": [
            "A) «Tirik axloq» (Agni yoga), «Krishnani anglash jamiyati», «Transsendental' meditasiya», «Aum-Sinrikyo», «Saxadja-yoga»",
            "B) «Runvira» ukrain milliy e'tiqodi cherkovi, Rossiya jarangli kedrlari, Omsk «qadimgi diniy e'tiqodiga qaytish kul'ti»",
            "C) «Mun birlashtirish cherkovi», «Vissarion oxirgi Ahdi cherkovi», «Oq birodarlar»",
            "D) «Xristian ilmi», «Ron Xabbard sayentologiya markazi», «Kloneyd», «Oq ekologlar» harakati"
        ],
        "togri": "A"
    },
    {
        "savol": "Yangi majusiy tashkilot va kul'tlar -",
        "variantlar": [
            "A) «Mun birlashtirish cherkovi», «Vissarion oxirgi Ahdi cherkovi», «Oq birodarlar»",
            "B) «Tirik axloq» (Agni yoga), «Krishnani anglash jamiyati», «Transsendental' meditasiya», «Aum-Sinrikyo», «Saxadja-yoga»",
            "C) «Runvira» ukrain milliy e'tiqodi cherkovi, Rossiya jarangli kedrlari, Omsk «qadimgi diniy e'tiqodiga qaytish kul'ti»",
            "D) «Xristian ilmi», «Ron Xabbard sayentologiya markazi», «Kloneyd», «Oq ekologlar» harakati"
        ],
        "togri": "C"
    },
    {
        "savol": "Imom Buxoriy hayoti davomida",
        "variantlar": [
            "A) 650 ming hadis to‘plab, ulardan 7275 hadisni o‘zining 4 jildlik «Ishonarli to‘plam»iga kiritdi",
            "B) 600 ming hadis to‘plab, ulardan 7275 hadisni o‘zining 4 jildlik «Ishonarli to‘plam»iga kiritdi",
            "C) 600 ming hadis to‘plab, ulardan 7175 hadisni o‘zining 4 jildlik «Ishonarli to‘plam»iga kiritdi",
            "D) 600 ming hadis to‘plab, ulardan 7275 hadisni o‘zining 5 jildlik «Ishonarli to‘plam»iga kiritdi"
        ],
        "togri": "B"
    },
    {
        "savol": "Shariat -",
        "variantlar": [
            "A) «yo‘nalish» ma'nosini bildirib, Islom atamashunosligida biror diniy masala, muammo bo‘yicha muayyan ulamo fikriga ergashish, «uning yurgan yo‘nalishidan borish» ni bildiradi",
            "B) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, ibodat yo‘llari, hayotiy va ijtimoiy qoidalar, kishilar orasidagi munosabat va muammolar, halol bilan haromni ajratib bermoqdir",
            "C) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun. Qiyomat kuniga iymon keltirish islom dinining muhim unsurlaridan biridir",
            "D) «ahira» so‘zidan «oxir», «keyin bo‘ladigan narsa», «oxirgi kun» degan ma’nolarni bildiradi. Musulmonlar bu so‘zni bu yerdagi dunyoning oxiri, shuningdek, o‘limdan keyin boshlanadigan yangi, cheksiz hayot deb atashadi"
        ],
        "togri": "B"
    },
    {
        "savol": "Mazhab so‘zi (arabcha - zaxaba 'ala mazhabixi)",
        "variantlar": [
            "A) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun. Qiyomat kuniga iymon keltirish islom dinining muhim unsurlaridan biridir",
            "B) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, ibodat yo‘llari, hayotiy va ijtimoiy qoidalar, kishilar orasidagi munosabat va muammolar, halol bilan haromni ajratib bermoqdir",
            "C) «yo‘nalish» ma'nosini bildirib, Islom atamashunosligida biror diniy masala, muammo bo‘yicha muayyan ulamo fikriga ergashish, «uning yurgan yo‘nalishidan borish» ni bildiradi",
            "D) «ahira» so‘zidan «oxir», «keyin bo‘ladigan narsa», «oxirgi kun» degan ma’nolarni bildiradi. Musulmonlar bu so‘zni bu yerdagi dunyoning oxiri, shuningdek, o‘limdan keyin boshlanadigan yangi, cheksiz hayot deb atashadi"
        ],
        "togri": "C"
    },
    {
        "savol": "Oxirat arabcha",
        "variantlar": [
            "A) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun. Qiyomat kuniga iymon keltirish islom dinining muhim unsurlaridan biridir",
            "B) «ahira» so‘zidan «oxir», «keyin bo‘ladigan narsa», «oxirgi kun» degan ma’nolarni bildiradi. Musulmonlar bu so‘zni bu yerdagi dunyoning oxiri, shuningdek, o‘limdan keyin boshlanadigan yangi, cheksiz hayot deb atashadi",
            "C) «yo‘nalish» ma'nosini bildirib, Islom atamashunosligida biror diniy masala, muammo bo‘yicha muayyan ulamo fikriga ergashish, «uning yurgan yo‘nalishidan borish» ni bildiradi",
            "D) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, ibodat yo‘llari, hayotiy va ijtimoiy qoidalar, kishilar orasidagi munosabat va muammolar, halol bilan haromni ajratib bermoqdir"
        ],
        "togri": "B"
    },
    {
        "savol": "«Qiyomat» arabcha",
        "variantlar": [
            "A) to‘g‘ri yo‘lga solmoq, qonunchilik yo‘naltirmoq, ibodat yo‘llari, hayotiy va ijtimoiy qoidalar, kishilar orasidagi munosabat va muammolar, halol bilan haromni ajratib bermoqdir",
            "B) «ahira» so‘zidan «oxir», «keyin bo‘ladigan narsa», «oxirgi kun» degan ma’nolarni bildiradi. Musulmonlar bu so‘zni bu yerdagi dunyoning oxiri, shuningdek, o‘limdan keyin boshlanadigan yangi, cheksiz hayot deb atashadi",
            "C) «yo‘nalish» ma'nosini bildirib, Islom atamashunosligida biror diniy masala, muammo bo‘yicha muayyan ulamo fikriga ergashish, «uning yurgan yo‘nalishidan borish» ni bildiradi",
            "D) tik turgan kun - islom esxatologiyasida Alloh taoloning hukmi kuni, barcha insonlar qilmishlari uchun jazo oladigan kun. Qiyomat kuniga iymon keltirish islom dinining muhim unsurlaridan biridir"
        ],
        "togri": "D"
    },
    {
        "savol": "Molikiylikning kitobi",
        "variantlar": [
            "A) «Al-Umm»",
            "B) «Al-Muvatta»",
            "C) «Al-Musnad»",
            "D) «Al-Kofiy»"
        ],
        "togri": "B"
    },
    {
        "savol": "Shofe'iylikning kitobi",
        "variantlar": [
            "A) «Al-Musnad»",
            "B) «Al-Muvatta»",
            "C) «Al-Umm»",
            "D) «Al-Kofiy»"
        ],
        "togri": "C"
    }
]

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ===== NATIJALAR =====
def natija_saqlash(ism, soni, togri, notogri):
    natijalar = []
    if os.path.exists(NATIJALAR_FAYL):
        try:
            with open(NATIJALAR_FAYL, 'r', encoding='utf-8') as f:
                natijalar = json.load(f)
        except:
            natijalar = []
    
    natijalar.append({
        "ism": ism,
        "sana": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "jami": soni,
        "togri": togri,
        "notogri": notogri
    })
    
    with open(NATIJALAR_FAYL, 'w', encoding='utf-8') as f:
        json.dump(natijalar, f, ensure_ascii=False, indent=2)

def natijalar_olish():
    if not os.path.exists(NATIJALAR_FAYL):
        return []
    try:
        with open(NATIJALAR_FAYL, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# ===== KLAVIATURALAR =====
def bosh_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Testni boshlash")],
            [KeyboardButton(text="📊 Natijalar"), KeyboardButton(text="ℹ️ Bot haqida")]
        ],
        resize_keyboard=True
    )

def variant_klaviatura():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="A"), KeyboardButton(text="B")],
                  [KeyboardButton(text="C"), KeyboardButton(text="D")]],
        resize_keyboard=True
    )

# ===== HOLATLAR =====
class TestState(StatesGroup):
    ism = State()
    soni = State()
    test = State()

# ===== HANDLERLAR =====
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Salom! Dinshunoslik test botiga xush kelibsiz!\n\n"
        f"📚 Jami {len(TESTS)} ta savol mavjud\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=bosh_menu()
    )

@dp.message(F.text == "ℹ️ Bot haqida")
async def bot_haqida(message: types.Message):
    await message.answer(
        "ℹ️ *Dinshunoslik Test Boti*\n\n"
        f"📚 Savollar soni: {len(TESTS)} ta\n"
        "🎯 Maqsad: Dinshunoslik fanidan bilimlarni sinash\n"
        "⏱ Har bir test oldidan 10 soniya tayyorlanish vaqti beriladi\n\n"
        "🚀 Boshlash uchun \"Testni boshlash\" tugmasini bosing!",
        reply_markup=bosh_menu()
    )

@dp.message(F.text == "📊 Natijalar")
async def natijalar(message: types.Message):
    barcha = natijalar_olish()
    if not barcha:
        await message.answer("📊 Hali hech kim test yechmagan!", reply_markup=bosh_menu())
        return
    
    # Oxirgi 10 ta natija
    oxirgi = barcha[-10:][::-1]
    matn = "📊 *So'nggi natijalar:*\n\n"
    for i, n in enumerate(oxirgi, 1):
        foiz = round(n["togri"] / n["jami"] * 100)
        matn += (
            f"{i}. 👤 {n['ism']}\n"
            f"   📅 {n['sana']}\n"
            f"   ✅ {n['togri']}/{n['jami']} ({foiz}%)\n\n"
        )
    await message.answer(matn, reply_markup=bosh_menu())

@dp.message(F.text == "🚀 Testni boshlash")
async def test_boshlash(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "📝 Ism va familiyangizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(TestState.ism)

@dp.message(TestState.ism)
async def ism_olish(message: types.Message, state: FSMContext):
    await state.update_data(ism=message.text)
    await message.answer(
        f"✅ Rahmat, {message.text}!\n\nNechta test yechmoqchisiz? (1 dan {len(TESTS)} gacha):"
    )
    await state.set_state(TestState.soni)

@dp.message(TestState.soni)
async def soni_olish(message: types.Message, state: FSMContext):
    try:
        soni = int(message.text)
        if soni < 1 or soni > len(TESTS):
            await message.answer(f"❗ Iltimos, 1 dan {len(TESTS)} gacha son kiriting:")
            return
    except:
        await message.answer("❗ Iltimos, faqat son kiriting:")
        return

    tanlangan = random.sample(TESTS, soni)
    await state.update_data(soni=soni, joriy=0, togri=0, notogri=0, tanlangan=tanlangan)

    msg = await message.answer("🕐 Test boshlanmoqda...\n\n⏳ 10")
    for i in range(9, 0, -1):
        await asyncio.sleep(1)
        await msg.edit_text(f"🕐 Test boshlanmoqda...\n\n⏳ {i}")
    await asyncio.sleep(1)
    await msg.edit_text("🚀 TEST BOSHLANDI!")

    await state.set_state(TestState.test)
    await savol_yuborish(message, state)

async def savol_yuborish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    joriy = data["joriy"]
    soni = data["soni"]
    tanlangan = data["tanlangan"]

    if joriy >= soni:
        togri = data["togri"]
        notogri = data["notogri"]
        ism = data["ism"]
        foiz = round(togri / soni * 100)
        
        natija_saqlash(ism, soni, togri, notogri)
        
        if foiz == 100:
            baho = "🎉 Ajoyib! Mukammal natija!"
        elif foiz >= 80:
            baho = "👍 Yaxshi natija!"
        elif foiz >= 60:
            baho = "😊 O'rtacha natija"
        else:
            baho = "📚 Ko'proq o'qish kerak!"

        await message.answer(
            f"🏁 TEST YAKUNLANDI!\n\n"
            f"👤 Ishtirokchi: {ism}\n"
            f"📅 Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            f"📊 Natija:\n"
            f"✅ To'g'ri: {togri} ta\n"
            f"❌ Noto'g'ri: {notogri} ta\n"
            f"📝 Jami: {soni} ta savol\n"
            f"📈 Foiz: {foiz}%\n\n"
            f"{baho}",
            reply_markup=bosh_menu()
        )
        await state.clear()
        return

    test = tanlangan[joriy]
    variantlar = "\n".join(test["variantlar"])
    await message.answer(
        f"❓ {joriy+1}-savol ({joriy+1}/{soni}):\n\n"
        f"{test['savol']}\n\n{variantlar}",
        reply_markup=variant_klaviatura()
    )

@dp.message(TestState.test, F.text.in_(["A", "B", "C", "D"]))
async def javob_olish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    joriy = data["joriy"]
    tanlangan = data["tanlangan"]
    test = tanlangan[joriy]
    javob = message.text.upper()

    if javob == test["togri"]:
        await message.answer("✅ To'g'ri javob!")
        await state.update_data(togri=data["togri"]+1)
    else:
        togri_variant = next(v for v in test["variantlar"] if v.startswith(test["togri"]))
        await message.answer(f"❌ Noto'g'ri!\n✅ To'g'ri javob: {togri_variant}")
        await state.update_data(notogri=data["notogri"]+1)

    await state.update_data(joriy=joriy+1)
    await savol_yuborish(message, state)

@dp.message(TestState.test)
async def noto_gri_kiritish(message: types.Message):
    await message.answer("❗ Faqat A, B, C yoki D tugmasini bosing!")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
